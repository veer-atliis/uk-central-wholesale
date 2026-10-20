# Website stock ordering — test investigation

Date: 2026-10-20 (Australia/Perth).

## Request and authority

Veer requested investigation of products with an “Out of stock” ribbon appearing early in the shop. Veer supplied an admin session in `https://veer-testing.odoo.com` and authorised testing and code changes if required. Work was performed by the assistant on Veer's behalf. No production changes were authorised or performed.

## Evidence

- Production shop inspection: Featured sort targets `website_sequence asc`.
- Supplied product screenshots: BAJ350 and RGJ350 both track inventory and have zero on hand, with website sequences 9 and 11 respectively. Only BAJ350 has the Out of stock ribbon.
- Test database identifies itself as neutralised and Odoo saas~19.4 Enterprise.
- Scheduled action 84, server action 1107: Website: sort in-stock products first (A-Z); scheduler user Nitin Jeshani; five-minute interval. Inactive in the neutralised copy.
- Executed the original action manually in the test database without an execution error.
- Diagnostics under the scheduler account found 797 saleable product templates, zero tracked products with positive free stock, and zero products with positive on-hand quantity. Elevated read checks also returned zero positive quantities.
- There were zero internal-location stock quants in the test database.
- The two products in the first group were non-stock-tracked Donation and Service on Timesheets, sequences 1 and 2.
- BAJ350: tracked, on hand 0, free 0, sequence 9. RGJ350: tracked, on hand 0, free 0, sequence 11. FS09: tracked, on hand 0, free 0, sequence 14.
- Neerabup Warehouse exists. Website warehouse field returned empty in this test copy; this was not changed.

## Validation

Temporarily replaced the inactive action's code with diagnostic and test harnesses. The test harness used temporary stock quants in Neerabup's stock location and the original sorting code, then deliberately raised an exception to roll back all test stock and sequence changes.

Passed:

1. FS09 with five free units sorts before BAJ350 with five on hand fully reserved.
2. All 797 products receive the expected stock-group then name/ID sequence.
3. A repeat run retains the same ordering.
4. Releasing BAJ350's reservation and depleting FS09 promotes BAJ350 and demotes FS09.

The first transition test retained cached quantities after direct quant writes within the same transaction. The harness was corrected to invalidate the ORM cache between simulated runs, and all checks then passed. This was a test-harness issue, not a demonstrated defect in the scheduled action.

Subsequent verification confirmed zero internal stock quants remained and BAJ350 returned to sequence 9. Restored the original 13-line action code, saved it, and ran it successfully. The action remains inactive as found in the neutralised database. Diagnostic exceptions may appear in test execution history; they were intentional rollback/reporting mechanisms.

## Outcome and limits

No sorting-code defect was demonstrated. The current test data puts nearly the entire catalogue in the out-of-stock group, which is then ordered alphabetically. A missing ribbon is not evidence of available inventory.

This confirms manual execution and classification behaviour in the test copy, not production scheduler health or production-wide inventory balances. The test copy's missing stock records must not be assumed to describe live inventory without confirmation.

Suggested next decision: establish whether website availability should follow maintained Odoo free stock or a separately maintained availability indicator. If inventory is authoritative, maintain accurate stock data and align ribbons with the same availability definition. If the business intentionally uses ribbons as its availability record, agree that rule before replacing the current stock-based sorting criterion.

Evidence screenshot: [Restored test action](scheduled-action-restored.png).

## Follow-up: authorised ribbon-based ordering

Veer subsequently explicitly requested changing the test action to place products with the “Out of stock” ribbon last, with both groups sorted A–Z.

Updated action 84 and renamed it **Website: Out of stock ribbon last (A-Z)**. The saved implementation is [ribbon-sort.py](ribbon-sort.py). It retains the saleable-product scope and scheduler user, identifies the ribbon by its English name with an exact case-insensitive match, and sorts each group case-insensitively by product name with ID as a tie-breaker. It stops with an explanatory error if the ribbon cannot be found. Only changed website sequences are written; quantities and ribbon assignments are not changed by the final code.

Executed the updated action successfully and verified all 797 products:

- 448 without that ribbon precede 349 with it.
- Saved sequence order matches the complete expected A–Z grouping.
- Repeating the action changes zero sequence values.
- A temporary test removing BAJ350's ribbon and assigning it to RGJ350 correctly promoted BAJ350 and demoted RGJ350. These temporary ribbon and sequence changes were deliberately rolled back.
- Baseline after the applied update: RGJ350 sequence 1, BAJ350 sequence 449.
- The refreshed test storefront in Featured order starts with RGJ350, After Eight, Ariel, Ballymaloe and Barratt products; none of the 21 first-page products displays the Out of stock ribbon.

Restored and saved the final ribbon-sorting code after the test harness. The action remains inactive in the neutralised test database; the five-minute interval is retained. Validation used manual execution, not a timed scheduler run. Production remains unchanged.

Screenshot: [Updated test shop first page](ribbon-sorting-first-page.png).

## Follow-up: two active actions using free stock

Veer authorised setting up both actions in the test database using on-hand stock minus reservations, with ribbon updates before sorting.

Final configuration:

| Action | ID | Interval | Priority | Scheduler user | Active |
|---|---|---|---|---|---|
| Website: sync Out of stock ribbon (free stock) | 83 | 5 minutes | 4 | Nitin Jeshani | Yes |
| Website: Out of stock ribbon last (A-Z) | 84 | 5 minutes | 5 | Nitin Jeshani | Yes |

The sorting code explicitly calls action 83's server action before sorting, so execution order does not rely solely on priorities or timing. The standalone ribbon schedule also refreshes labels independently. Both use the same scheduler account. The lookup requires exactly one action with the configured ribbon-update name; keep this name aligned if renaming it.

Ribbon rules:

- Active saleable, inventory-tracked products with free stock at or below zero receive Out of stock.
- Products with positive free stock, or products not tracked in inventory, have this ribbon removed if present.
- Out of stock takes precedence over another assigned ribbon when stock is unavailable. Removing it later clears the field; it does not restore an earlier promotional ribbon.
- Other ribbons on available products are retained.
- Both actions include unpublished saleable products, ensuring consistent classification before publication.
- Availability is evaluated in the current company's sole warehouse, currently Neerabup. The action stops with an explanatory error if there is no single warehouse or no unique matching English Out of stock ribbon.
- Stock quantities, purchasing permissions, and quantity-display settings are not changed by the final actions.

Files: [ribbon updater](free-stock-ribbon-sync.py), [sorting action including updater call](ribbon-sort.py).

Integrated validation ran under Nitin's scheduler context, using temporary stock records and deliberate transaction rollback. Passed zero, negative, fully reserved and positive free-stock scenarios; full-catalogue ribbon consistency and ordering across 797 products; repeat-run stability; reservation release; and stock depletion. The temporary harness was removed before activation.

Both final actions were saved and enabled. Manually executed the final combined sorting action and the standalone ribbon updater successfully. Refreshed Featured storefront order shows alphabetically ordered Out of stock-labelled products, as expected for the copy's zero-stock data. This supersedes the previous first-page result where only manually assigned ribbons were used. Timed unattended scheduler execution has not separately been observed.

Evidence: [enabled ribbon action](free-stock-ribbon-action.png), [paired storefront result](paired-actions-storefront.png).

All changes remain in `veer-testing.odoo.com`; production was not changed.

## Handover

Veer requested final code/settings for manual application to live and a retained work record. Prepared [Live setup.md](Live%20setup.md), with deployment steps, dependencies, validation limits and rollback guidance, alongside the two final Python code files.

Veer also requested updating `origin/main`. Initial checks in the OneDrive chat workspace returned “not a git repository”.

On 2026-10-21, the registered project was located at `D:\Atliis Files\Codex & Github\uk-central-wholesale`, with origin `https://github.com/veer-atliis/uk-central-wholesale.git`. Its `main` branch was clean and matched fetched `origin/main` at `ca0c481` before adding this package. Veer authorised copying the final automation code, settings, testing notes and supporting screenshots into that repository and pushing to `origin/main`. This resolves the earlier repository-location blocker. Publishing these records does not constitute live Odoo deployment.
