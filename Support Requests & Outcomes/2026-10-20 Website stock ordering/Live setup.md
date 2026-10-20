# Live setup — website availability automations

Prepared for Veer on 2026-10-20 (Australia/Perth). This is a deployment guide, not a record of live deployment. Production has not been changed by the assistant.

## Objective

Use free stock (on hand minus reservations) to maintain the Out of stock ribbon. Show products without that ribbon first, then products with it, with case-insensitive A–Z ordering within each group.

## Final settings and code

Update the two existing scheduled actions rather than creating duplicates.

| Setting | Ribbon update | Sorting |
|---|---|---|
| Exact action name | Website: sync Out of stock ribbon (free stock) | Website: Out of stock ribbon last (A-Z) |
| Model | Product (`product.template`) | Product (`product.template`) |
| Action type | Execute Code | Execute Code |
| Scheduler user | Nitin Jeshani | Nitin Jeshani |
| Interval | 5 minutes | 5 minutes |
| Priority | 4 | 5 |
| Allowed Groups | Leave blank, as tested | Leave blank, as tested |
| Active | Enable after saving and validating both actions | Enable after saving and validating both actions |
| Next execution | Choose a near-future time | Same time as ribbon update |

Paste the complete contents of [free-stock-ribbon-sync.py](free-stock-ribbon-sync.py) into the ribbon action and [ribbon-sort.py](ribbon-sort.py) into the sorting action.

The sorting action locates the ribbon update by its exact name and calls it before sorting. This provides execution order even for manual runs; the two priorities alone do not establish a dependency. Disabling only the ribbon schedule does not stop the sorting action from calling its code. Disable both to stop the pair.

## Apply and check

1. Save the existing action code/settings and export current product ribbon assignments and website sequences if rollback to the existing presentation is required.
2. Confirm live Odoo stock quantities and reservations are maintained accurately. The test copy contained no internal stock records; do not assume the same is true in production.
3. Confirm the scheduler's current company is UK Central Wholesale, with exactly one warehouse (Neerabup), and exactly one ribbon named Out of stock in English. The code stops if these assumptions fail. Nitin needs the relevant product, inventory, ribbon and scheduled/server-action access, as exercised in the test copy.
4. Keep both schedules inactive while replacing code and settings. Save the ribbon update first using its exact name, then save sorting.
5. Run the sorting action manually. It runs the ribbon update first and then sorts.
6. Check a product with positive free stock and one with zero/negative free stock. The first should have no Out of stock ribbon; the second should have it. Confirm the shop uses Featured sorting, with the latter group after the former and A–Z within each group.
7. Enable both schedules, with the next execution at the same near-future time in the user's displayed timezone. Refresh after the due time and verify execution dates advance and results remain correct.

## Behaviour to retain

- Scope: active saleable product templates, including unpublished products.
- Non-stock-tracked products are not labelled Out of stock.
- Out of stock replaces another assigned ribbon when free stock is zero or negative. The previous promotional ribbon is not stored or restored.
- When stock becomes available, only the Out of stock ribbon is cleared; other current ribbons are preserved.
- Manual website sequencing is overwritten.
- Quantities, orderability settings and quantity display settings are not changed.
- No numeric ribbon/action IDs from the test database need to be copied.

## Validation and rollback

Integrated test-database checks passed for zero, negative, positive and fully reserved stock; releasing reservations; depleting stock; full-catalogue grouping/A–Z order; and repeat-run stability. Both final actions were enabled and executed manually successfully. Unattended timed execution has not separately been observed.

Disable both actions to stop further changes. Restoring old code alone does not restore prior ribbon assignments or website sequences; use the saved presentation export if needed.

See [Investigation.md](Investigation.md) for findings and the complete work record.

## Repository publication

On 2026-10-21, the correct project repository was located at `D:\Atliis Files\Codex & Github\uk-central-wholesale`, with origin `https://github.com/veer-atliis/uk-central-wholesale.git`. Veer authorised publishing this automation package to `origin/main`. The original OneDrive chat workspace was not a Git repository; that earlier location issue is resolved.

Repository publication records the code, settings and test evidence. It does not deploy the actions to the live Odoo database.
