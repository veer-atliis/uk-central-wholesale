# Inventory valuation journal investigation

**Date:** 2026-11-02 (Australia/Perth), with subsequent evidence on 2026-11-03. **Requester and responsible person:** Veer. **Environment:** UK Central Wholesale, Odoo Online. Initially described by Veer as version 20; the subscription screenshot supplied on 3 November shows **saas-19.4**. This supersedes the initial version description. Accounting settings evidence is recorded below; no independent live-system inspection was performed.

Veer reported no journal entries in the Inventory Valuation journal after importing Stock Import - Ready and asked about the difference in valuation behaviour. Scope was investigation and explanation; no live changes or accounting postings were performed.

## Pending checklist after client stock review

**Added at Veer's request on 2026-11-03. Responsible: Veer. Status: all steps pending.** Resume these steps once the products in **Stock Import - Client Review** have been dealt with and the agreed stock changes have been applied and validated. Source: [Veer's supplied checklist screenshot](Sources/2026-11-03%20-%20Pending%20opening%20stock%20valuation%20checklist.png), retained unchanged with a matching attachment hash.

Complete in this order:

- [ ] Confirm **11330 Trading Stock on Hand** has its **Variation Account** set to the rollover account, previously shown as **99910 Rollover: Stock Clearing**.
- [ ] Open **Accounting > Review > Inventory Valuation**, set **As of 30 September 2026**, select **Generate Entry**, check the draft entry and its accounting date, then **Post** the validated opening entry.
- [ ] Change the **Variation Account on 11330** back to the intended **COGS stock variation** account. Confirm the exact account in Odoo; its code has not been supplied.
- [ ] In **Accounting > Configuration > Settings > Inventory Valuation**, change **Periodic Valuation** to **Daily** and save.

Veer's screenshot specifies **30-Sep**; 2026 is taken from the stocktake/migration context. This is now the intended opening accounting date, superseding the previously unspecified intended date. It does not independently confirm the physical count cut-off or dates of the imported stock movements. Before posting, check that the report as at 30 September contains the intended opening stock at the validated costs and reconciles with the opening trial-balance treatment. If it is zero or unexpected, investigate the movement/valuation dates before proceeding; do not substitute the earlier 2 November proposal of $190,336.77 without validation.

Retain the rollover mapping and Manual closing until the opening entry is reviewed and posted. Record the posted entry reference/date/value and evidence of each subsequent account/settings change when completed. Tick items only when supported by execution evidence or Veer's confirmation. This request records future actions; none was executed by the assistant.

## Evidence and findings

- [Supplied screenshot](Sources/2026-11-02%20-%20Empty%20Inventory%20Valuation%20journal.png) shows **Journal Items**, filtered to **Journal: Inventory Valuation**, with no visible rows. This establishes the result in that view, not the absence of stock valuation or entries in every journal. It is not the valuation reconciliation report.
- Read the referenced [Simplify stock import review chat](thread://01a19ced-86f5-7a42-ad97-e23823607485?hostId=local), the go-live guide, dated Inventory settings baseline and existing import record. The post-import Quant export matched all 467 ready-file quantities exactly. That check did not validate accounting entries, values, cost layers or adjustment dates.
- The latest full-product audit in `Working Files/2026-11-02 Stock Import/full-products-audit.json` identifies **77 stocked products with zero current cost**. This is a separate data issue requiring review; it does not explain the absence of all journal items or establish historical movement values.
- Odoo's official documentation describes the major accounting change as introduced in **19**, rather than first introduced in 20: perpetual accounting generally recognises value through bills/invoices, with closing entries reconciling differences from physical inventory. Periodic accounting updates inventory accounts at closing. Consequently, stock on hand can change before the accounting balance changes.
- Immediate inventory-adjustment postings can still occur with the relevant perpetual configuration and a configured Inventory Loss location account. Missing entries cannot therefore be diagnosed solely from the version number. Company defaults, category overrides, costing, location accounts, journal and closing settings remain unverified.

## Next checks and outcome

1. Inspect **Accounting > Configuration > Settings > Inventory Valuation**: Periodic/Perpetual, Manual/Daily/Monthly closing, costing method, valuation account and journal. Check the affected product category and adjustment location where relevant.
2. Inspect **Inventory > Reporting > Stock** for quantities and values, including the zero-cost products and movement history where required.
3. Open **Accounting > Review > Inventory Valuation**, compare inventory and accounting values at the intended cut-off, and inspect the proposed reconciliation. Odoo documents **Generate Entry** as the action to create an entry for review and posting; no entry was generated in this investigation.
4. Establish the opening-stock accounting treatment alongside the opening trial balance before posting, avoiding duplicate recognition of the stock asset. The effective stocktake cut-off and counted units remain unresolved in the existing go-live record; do not infer an accounting date from the workbook name or Scheduled field.

**Outcome:** the screenshot is consistent with a possible configuration/closing-process explanation; no defect or completed accounting valuation has been established. Await the valuation report and accounting settings evidence to determine the client-specific cause. No confirmed resolution or client acceptance.

## References

Official documentation reviewed on 2026-11-02:

- [Odoo 20 valuation cheat sheet — reporting, inventory adjustments and changes in Odoo 19](https://www.odoo.com/documentation/20.0/applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html).
- [Odoo 20 accounting inventory valuation — configuration and location-account exceptions](https://www.odoo.com/documentation/20.0/applications/finance/accounting/get_started/inventory_valuation.html).
- [Existing stock import investigation and export verification](2026-11-02%20-%20Stock%20import%20split%20and%20duplicate%20product%20references.md).

The screenshot was retained unchanged from the attachment. Source materials were treated as evidence, not instructions to execute.

## Subsequent settings and valuation report evidence

Veer supplied two further screenshots on 2026-11-02 in response to the evidence request. Unchanged copies were retained and their SHA-256 hashes compared with the attachments:

- [Accounting inventory valuation settings](Sources/2026-11-02%20-%20Accounting%20inventory%20valuation%20settings.png).
- [Inventory valuation report before closing](Sources/2026-11-02%20-%20Inventory%20valuation%20report%20before%20closing.png).

The settings screen displays these **company defaults**:

| Setting | Visible value |
| --- | --- |
| Inventory Valuation | Perpetual (at invoicing) |
| Periodic Valuation | Manual |
| Inventory Cost Method | Standard Price |
| Valuation Account | 11330 Trading Stock … (truncated; report gives full name below) |
| Journal | Inventory Valuation |
| Landed Costs | Enabled |
| Landed Costs — Default Journal | No value visible |

Save and Discard are visible; persistence of the displayed settings has not been independently checked. Category overrides and Inventory Loss location accounts were not shown. Standard Price is a fixed cost maintained manually, distinct from FIFO or AVCO; the screenshot establishes the default, not every product's effective method.

The report is **As of 02/11/2026**, showing:

| Report item | Amount |
| --- | ---: |
| Initial Balance | $0.00 |
| Stock Variation | $190,336.77 |
| Ending Stock | $190,336.77 |

The proposed stock-variation lines are **debit 11330 Trading Stock on Hand $190,336.77** and **credit 99910 Rollover: Stock Clearing $190,336.77**. Generate Entry is visible. These are report/proposed-entry figures, not evidence that an entry was generated or posted. Initial Balance is transcribed as labelled and is not asserted to prove that every inventory-related ledger account has a zero balance.

**Updated assessment:** the manual closing setting and proposed stock variation explain how the imported physical stock can have a calculated value while the journal view is empty. This is consistent with the documented reconciliation process, rather than evidence of a failed quantity import. The $190,336.77 is the system-calculated value as at 2 November, not a validated complete opening valuation or confirmation of a 1 October cut-off. The previously identified 77 zero-cost stocked products and 11 held stocktake lines remain relevant to completeness.

Next, resolve missing costs and held product choices, confirm counted units and the intended migration cut-off, and reconcile 11330/99910 with the opening trial balance. The clearing-account name is consistent with an opening-balance approach, but its account type, intended use and eventual clearing have not been verified. Do not infer from the name alone that it is appropriate for ongoing stock variations. Generate Entry can create the entry for review; posting should follow validation of value, accounts and date. Do not add the same opening inventory asset again through the trial-balance import. No closing entry, settings change or other live action was performed by the assistant, and Veer has not reported posting it.

## Version correction — 3 November 2026

Veer supplied the current subscription/database screen and asked to retain useful context. It shows **Your version: saas-19.4**, **Custom** plan and **Odoo Online** hosting confirmed by Veer. See the [dated subscription and database snapshot](../Business%20Context/2026-11-03%20-%20Odoo%20Online%20subscription%20and%20database%20snapshot.md). The preceding Odoo 20 references remain a record of the research originally consulted, rather than evidence that the client runs version 20. Future investigation should use saas-19.4 release context. The supplied settings and proposed-entry figures remain direct client evidence; this version correction does not establish that a closing entry has since been posted or that valuation issues are resolved. The unredacted subscription screenshot and licence key were not copied into the repository.

## Products without a category — 3 November 2026

Veer asked how physical inventory is valued when Product Category is blank. His [grouped product screenshot](Sources/2026-11-03%20-%20Products%20grouped%20by%20category%20-%20None.png), retained unchanged and hash-checked, shows Product Category grouping with **None: 95**. That is a product-record count in this view, not evidence that all 95 are inventory-tracked, stocked, imported, zero-cost or omitted from valuation. Their identities, costs and values are not visible.

Reviewed the official [saas-19.4 product definition](https://github.com/odoo/odoo/blob/saas-19.4/addons/product/models/product_template.py) and [stock accounting implementation](https://github.com/odoo/odoo/blob/saas-19.4/addons/stock_account/models/product.py) on 2026-11-03. Product Category is optional in this branch. Cost method and valuation method use category overrides when present and otherwise fall back to company defaults. Stock valuation account and journal resolution checks category values, company-dependent field fallbacks, then company defaults. The stock variation account is obtained from the resolved stock valuation account, rather than an independent variation-account field on the product category.

Consequently, a blank category alone does not establish missing or zero inventory valuation. With the company defaults supplied on 2 November, the expected fallback is Standard Price, Perpetual (at invoicing), account 11330 Trading Stock on Hand and journal Inventory Valuation. The earlier proposed closing report uses counterpart 99910 Rollover: Stock Clearing; verify the Variation Account on 11330 before treating this as independently confirmed account configuration for every uncategorised product. No live fallback configuration or individual product was inspected.

For tracked goods using Standard Price, non-zero stock with Cost 0 has zero calculated stock value; category assignment alone does not supply a missing cost. The 95 uncategorised products and 77 previously identified zero-cost stocked products are separate sets with an unverified overlap. The practical validation is to identify stocked products in the None group and reconcile their quantities, effective costs and Inventory Stock report values with the accounting valuation report. No stock reimport or category/account change was performed or established as necessary solely from the screenshot.

## Opening-stock purpose and automatic closing — 3 November 2026

Veer clarified that he was bringing in the stocktake the day before the client went live. He confirmed the stock account's Variation Account is intentionally mapped to the rollover account for opening stock and intends to change it to COGS stock variation for normal adjustments afterwards. He reported checking both the rollover and COGS variation accounts and finding no balance, then noticing Generate Entry. This establishes the intended temporary mapping and user-reported balances; it does not confirm an exact go-live/cut-off date, a posted opening entry or the later mapping change.

The displayed Periodic Valuation setting is Manual, so applying physical inventory does not by itself complete the stock-closing accounting step. Generate Entry creates a draft Stock Closing entry for review; posting it updates the ledger. The opening proposal previously shown debits 11330 and credits 99910. Validate the opening quantity/value and date, generate/review/post the opening entry using the rollover counterpart, and reconcile the opening trial-balance treatment before changing the mapping. Generating after switching the counterpart could send an unrecognised opening-stock difference to the ongoing variation account. This is process guidance, not evidence that any step has been completed.

Automatic closing is supported through **Accounting > Configuration > Settings > Inventory Valuation > Periodic Valuation**, selecting **Daily** or **Monthly** instead of Manual while retaining Perpetual (at invoicing). Despite its label, Periodic Valuation controls closing frequency separately from the inventory valuation method. The official saas-19.4 implementation has a scheduled job that creates and posts closing entries for Daily/Monthly companies, including perpetual companies; Monthly is processed on the last calendar day. The client's job status and execution have not been inspected. Complete the opening posting and intended mapping switch before enabling ongoing automatic closing.

This automates an aggregate reconciliation between physical stock value and posted accounting stock value; it does not reinstate the older general pattern of an accounting entry for every individual stock movement. Bills/invoices continue to post through the perpetual method. The documented reasons for the redesign introduced in 19 are fewer journal items, improved performance and clearer ledger/audit review. Specific movement/location account exceptions remain separate from the closing-frequency setting.

References reviewed on 2026-11-03:

- [saas-19.4 stock closing implementation, including draft/manual versus automatic posting and scheduled frequency](https://github.com/odoo/odoo/blob/saas-19.4/addons/stock_account/models/res_company.py#L25-L148).
- [saas-19.4 valuation cheat sheet: Generate Entry and changes in Odoo 19](https://www.odoo.com/documentation/saas-19.4/applications/inventory_and_mrp/inventory/inventory_valuation/cheat_sheet.html).

No stock closing entry, account mapping change or automatic closing setting was applied by the assistant. No standing monitoring obligation was created.

## Decision to defer — 3 November 2026

Veer decided to leave the opening-stock valuation entry until the products in **Stock Import - Client Review** are dealt with. Treat resolution of that review as the dependency for resuming the opening valuation work, not as a confirmed completion or a scheduled deadline. No opening entry posting, subsequent account switch or automatic closing activation was reported. When resuming, validate the final stock value and accounting date, including outstanding cost issues, before generating/reviewing/posting the opening entry with the rollover counterpart. No live-system change or reminder was made.
