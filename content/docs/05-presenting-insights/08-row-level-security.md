---
title: Interactive row level security
url: /docs/presenting-insights/interactive-row-level-security/
description: Learn how to preserve unit-record interactivity and population context when implementing row level security in Power BI.
lede: RLS should limit access without destroying unit-record interactivity.
weight: 8
# draft: true
---

## Security without losing context

Row level security (RLS) in Power BI means exposing to users only the rows they are allowed to see. This is implemented through a DAX filter attached to the user’s security role.

The important subtlety is that an RLS filter is not visible to DAX as an ordinary, inspectable filter. Functions such as `isfiltered()` or `isinscope()` cannot detect that RLS is active. A formula simply evaluates over the rows available to the user after security has been applied.

This makes restriction straightforward but comparison difficult. If a regional user is restricted to regional rows, then ordinary measures automatically evaluate over that regional population. A national comparison cannot be recovered by asking DAX to notice and remove the RLS filter. The wider population must be deliberately modelled.

A common solution is to summarise the wider population into aggregate tables. This can reduce disclosure risk, and it may be the right approach for highly sensitive data. However, summary tables do not preserve unit-record interactivity. They also introduce their own modelling complexity, because every supported comparison must be anticipated in the summary design.

This chapter focuses on approaches that preserve unit-record interactivity while still allowing comparison with a wider population.

This leads to two distinct tasks in implementing RLS:

- limiting what users can see;
- preserving population context.

## Limiting what users can see

RLS first needs an access-control pattern. There are two common approaches:

- static roles;
- dynamic roles.

This choice determines how the permitted population is assigned to each user.

### Static roles

Static roles use one RLS role per access category.

For example, the model may have separate roles for `North`, `South`, `West`, and `Unlimited`.

The `North` role may apply this filter to `'Region'`:

```DAX
'Region'[Region name] = "North"
```

The `South` role may apply:

```DAX
'Region'[Region name] = "South"
```

The `West` role may apply:

```DAX
'Region'[Region name] = "West"
```

The `Unlimited` role has no filter. Users assigned to this role can see all rows allowed by the model.

This is simple to understand and easy to test. Each role has its own DAX filter, and users are assigned to the role that matches their access.

The weakness is maintenance. Static roles work when the access categories are few and stable. They become awkward when users have many different access combinations, when access changes often, or when permissions need to follow organisational hierarchy.

A clear naming convention is important. `Limited` and `Unlimited` are often clearer than `Restricted` and `Unrestricted`, because `restricted` can mean either access to restricted data or restriction from data.

### Dynamic roles

Dynamic roles use a security mapping table and the user’s identity, usually through `userprincipalname()`.

Instead of creating one role per access category, the model has a role that looks up which rows the current user is allowed to see. The mapping table may connect users to regions, teams, programs, customers, or other secured entities.

For example, a simple user-region mapping table may look like this.

**Example structure of `'User access'`**

| User principal name | Region |
|---|---|
| alice@example.com | North |
| ben@example.com | South |
| clara@example.com | West |
| dana@example.com | North |
| dana@example.com | South |
| dana@example.com | West |

The RLS rule can then filter the model by the regions assigned to the current user.

A DAX expression may look like this:

```DAX
'User access'[User principal name] = userprincipalname ()
```

In practice, the filter often applies through relationships from the access table to a secured dimension or directly to the fact table.

Dynamic roles are more flexible and auditable. They allow access rules to be maintained in data rather than hard-coded into many RLS roles. They are especially useful when permissions are numerous, changing, hierarchical, or managed outside Power BI.

The trade-off is that the access table becomes part of the security infrastructure. It must be governed, tested, and documented. If the mapping logic is complex, the table should include metadata explaining why each assignment exists.

From a performance perspective, the filter should be applied as close as possible to the sensitive data. If the sensitive data resides in fact tables, the filter should ideally reach those fact tables directly. If the sensitive data resides in dimensions, the filter may apply through a snowflake relationship.

Multiple copies of the access table may be needed if filtering applies across multiple dimensions. In such cases, care must be taken to avoid conflicting filters that accidentally combine as an unintended `and` condition.

Whether access is static or dynamic, the result is the same: each user sees only their permitted rows. The harder problem is what happens when the user needs to compare those rows with a wider population.

## Preserving population context

RLS removes rows from the user’s visible population. If the user needs comparison against a wider population, that wider population must remain available through another modelling path.

For example, a regional team may need to compare its sales performance against national sales. The comparison may need to remain filterable by product type, sales period, customer segment, or other dimensions.

A measure such as this cannot recover rows removed by RLS:

```DAX
National sales volume =
calculate (
    [Sales volume],
    removefilters ( 'Sales team' )
)
```

`removefilters()` can remove ordinary filter context. It cannot bypass security. If RLS has already restricted the user to regional rows, then the national rows are not available to the measure.

There are two approaches to preserving population context while retaining unit-record interactivity:

- anonymous facts;
- pseudonymous dimensions.

### Anonymous facts

The anonymous approach duplicates the fact table and removes sensitive columns and sensitive relationship paths.

For example, suppose the model contains:

- a fact table `'Sales'`;
- a sensitive dimension `'Sales team'`;
- a measure `[Sales volume]`.

The restricted user should see only their permitted rows in `'Sales'`, but should also compare against the wider population.

The data engineer can create a second fact table:

- `'Sales anonymous'`

This table contains the population sales rows, but removes columns and relationships that identify the sensitive team or user. The relationship to `'Sales team'` is removed. Any sensitive columns are removed. The table is therefore not filtered by the same RLS path.

A population measure can then be defined over the anonymous fact:

```DAX
Population sales volume =
sum ( 'Sales anonymous'[Sales volume] )
```

The user-facing comparison measure might be:

```DAX
Regional sales proportion =
divide (
    [Sales volume],
    [Population sales volume]
)
```

The ordinary `[Sales volume]` measure reflects the user’s restricted rows. `[Population sales volume]` reflects the wider anonymous population. Both can still respond to safe shared dimensions such as calendar, product, or region grouping where appropriate.

For example, if both `'Sales'` and `'Sales anonymous'` relate to `'Calendar'` and `'Product'`, the user can still compare their regional sales with population sales by month and product type.

The anonymous approach preserves interactivity by keeping the population fact at the grain needed for analysis, while removing the sensitive columns and relationship paths that would identify restricted entities.

When there are many pairs of user and population measures, maintaining the measures can become tedious. The measure of measures pattern can help by creating one switch measure for restricted measures and another for population measures. Derived comparison measures can then be defined over the two switch measures rather than repeated for every metric.

### Pseudonymous dimensions

The pseudonymous approach assumes sensitive information is contained in dimensions.

For example, the sensitive information may be in `'Sales team'`, which contains team names, staff names, locations, or other identifying attributes.

Instead of duplicating the fact table, the data engineer duplicates the dimension rows through a union. One set of rows contains the real values. The other set contains masked values.

**Example structure of `'Sales team'`**

| Sales team SK | Sales team ID | Team name | Region | Is masked |
|---:|---|---|---|---|
| 1 | T001 | North Metro Team | North | false |
| 2 | T002 | South Coast Team | South | false |
| 101 | T001 | (masked) | North | true |
| 102 | T002 | (masked) | South | true |

The access table determines which doubled dimension rows each user principal may see. Since each `[Sales team ID]` has both a masked and unmasked row, the access table grants access to the appropriate `[Sales team SK]` for each user.

For example, one user may see the unmasked row for `T001` but the masked row for `T002`. Another user may have the reverse access. A national manager may see unmasked rows for all sales teams. The access table may look like this:

**Example structure of `'User sales team access'`**

| User principal name | Sales team SK |
|---|---:|
| alice@example.com | 1 |
| alice@example.com | 102 |
| ben@example.com | 101 |
| ben@example.com | 2 |
| clara@example.com | 1 |
| clara@example.com | 2 |

This user access table filters the `'Sales team'` dimension on `[Sales team SK]`. The RLS rule is applied to `'User sales team access'` using `[User principal name]`. The filtered access table then filters `'Sales team'` through `[Sales team SK]`, leaving only the masked or unmasked rows the user is allowed to see.

The relationship from the fact table to `'Sales team'`, based on `[Sales team ID]`, becomes many-to-many. Since `[Sales team SK]` has multiple values in the access table, it is also many-to-many.

The relationships can be summarised as a bus matrix.

| Dimension / access table | `'Sales team'` | `'Sales'` |
|---|---|---|
| `'User sales team access'` |  * → * via `[Sales team SK]` | |
| `'Sales team'` | |  * → * via `[Sales team ID]`  | 


Following the previous example, these would be the view for each user.

**Alice’s view**

| Team name | Region | Goals reached |
|---|---|---:|
| North Metro Team | North | 84 |
| (masked) | South | 57 |

**Ben’s view**

| Team name | Region | Goals reached |
|---|---|---:|
| (masked) | North | 84 |
| South Coast Team | South | 57 |

**Clara’s view**

| Team name | Region | Goals reached |
|---|---|---:|
| North Metro Team | North | 84 |
| South Coast Team | South | 57 |

In this case, each user can only see the full details of the teams they are granted access to. The fact table is unaffected because RLS is selecting visible dimension rows rather than removing fact rows directly. This means population measures can still use the same fact table through `removefilters()` where the security design permits it.

Care must be taken when masking. In some cases, the primary key itself is sensitive. For example, if the business key is a social security number or another identifying value, it should not be exposed as the relationship key. A surrogate key or non-sensitive mapping key is required.

The pseudonymous approach is lighter than duplicating facts, but it is also riskier. Because the same underlying facts remain available, an informed user may infer identities from distinctive combinations of values.

## Choosing an approach

The anonymous and pseudonymous approaches solve the same problem in different ways.

The anonymous approach duplicates the population facts and removes sensitive columns and relationship paths. It is safer and easier to reason about, but it increases model size and requires parallel population measures.

The pseudonymous approach doubles dimension rows and masks sensitive values. It keeps the model smaller and preserves the same fact table. However, because the same underlying fact rows remain available, it exposes more detail than the anonymous approach.

It is most useful when the identity of the row is not itself the main concern, but particular attributes need to be hidden. For example, a user may be allowed to see all traveller records and analyse their activity, but should not see sensitive values such as passport numbers, phone numbers, or personal identifiers.

Both approaches can preserve unit-level interactivity. This is intentional. The goal is to keep dimensional filtering, drillthrough, and detailed comparison available while limiting exposure of sensitive attributes.

This also means both approaches carry inference risk. A user may deduce identities from distinctive combinations of values, even when direct identifiers are removed or masked.

If that risk is unacceptable, the required design is no longer merely anonymous or pseudonymous RLS. It becomes a summary-table problem, with specific applications of mitigation strategies. This is outside the scope of this chapter.

The choice between anonymous population facts and pseudonymous dimensions is not purely technical. It reflects the organisation’s appetite for risk, governance requirements, security obligations, and expected user behaviour.



> [!NOTE]
> **Key ideas**
>
> RLS should limit access without destroying analytical context.
>
> DAX cannot detect RLS as an ordinary filter. Measures evaluate over the rows available after security has been applied.
>
> `removefilters()` cannot recover rows removed directly by RLS. Population context must be preserved through modelling design.
>
> RLS has two distinct tasks: limiting what users can see, and preserving population context.
>
> Anonymous population facts preserve wider population context by duplicating facts and removing sensitive columns and relationship paths.
>
> Pseudonymous dimensions preserve population context by masking sensitive dimension values while keeping the model interactive.
>
> Both anonymous and pseudonymous approaches preserve unit-record interactivity, but both carry inference risk.
