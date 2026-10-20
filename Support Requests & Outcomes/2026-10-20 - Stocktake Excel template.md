# Stocktake Excel template

Veer requested a simple Excel workbook on 2026-10-20 for the client to complete, allowing physical inventory counts to be prepared for Odoo import. Veer asked for coloured headers. Nitin is the primary client contact; no client acceptance or count date has been supplied.

## Evidence and design

- Supplied Inventory settings screenshot shows variants, units of measure and barcodes enabled. Lots/serial numbers, packages, consignment and storage locations appear disabled. Settings are observed in the screenshot only; the Save button is visible and saved database state was not independently checked.
- Odoo Online is confirmed by the project guide. Database version, actual product list, stock units, locations and import mappings have not been inspected.
- Created `Output/outputs/2026-10-20-stocktake/UK Central Wholesale - Stocktake Template.xlsx`, with Stocktake and Instructions tabs. There are 100 expandable blank rows, coloured headers, amber client entry columns, text-formatted identifiers and decimal quantity validation at or above zero.
- Veer prefills product/variant, internal reference, barcode, stock location, stock unit and the existing physical inventory record External ID. The client enters the total counted quantity and optional notes. Blank means not counted; zero is an explicit nil count.
- The workbook instructions use existing inventory record IDs (stock.quant), rather than product IDs, for updating counts. They retain Location as record context even though storage locations appear disabled. No location name, product data or packaging conversion has been invented.
- No lot, serial, package or owner fields are included. Items missing from the inventory export need separate preparation and verification. Do not assume an existing inventory export contains every product.

## Validation and next use

The workbook was generated and both tabs visually reviewed. Saved XLSX structure confirmed the two tabs, 100-row table, frozen header and numeric count validation. No live system access, import or stock adjustment was performed. Native Excel interaction has not been tested.

Later on 2026-10-20, Veer requested removal of the Instructions tab because instructions will be added to the knowledge article to which the workbook will be attached. Removed that tab. The delivered workbook now contains only Stocktake. Package verification confirmed the retained worksheet, table, styles and validation were unchanged byte-for-byte. No knowledge article was created or edited as part of this request.

Veer subsequently requested a very simple knowledge article and reported that the workbook could not be opened. Created the client article in `Output/Stocktake.md` for attachment in the knowledge system. Found undeclared compatibility namespace prefixes in workbook metadata following the worksheet-removal operation. Repaired that metadata while preserving all other ZIP parts byte-for-byte. XML and compatibility namespace checks passed. A direct local file link is supplied for opening the repaired file; native Excel opening remains to be confirmed.

The final repair also restored default namespaces in the package content-types and workbook relationship metadata after an Open XML reader rejected their prefixed form. Artifact Tool successfully reopened the repaired file. The current workbook has six columns: Internal Reference, Product / Variant, Unit of Measure, Counted Quantity, Notes and External ID. This differs from the earlier eight-column template; the repair preserved the current sheet, table, data and formatting without rebuilding them. Only the three metadata XML parts were changed. Native Excel opening remains unverified.

Veer then requested that the article contain only the client's steps and omit his name. Read the edited workbook without changing it: its identifier header is now Product System ID. Updated the article to match that header, removed named responsibilities and kept six short client steps. The header alone does not verify whether future populated IDs identify products or physical inventory records; confirm the actual ID type before preparing an import.

Before sharing for counting, Veer must prefill actual records and reconcile the count scope. After return, Veer prepares a values-only file containing External ID and Counted Quantity for completed counts only, retaining explicit zeros. Check duplicates, units and movements since counting. Confirm the actual database mapping, use Odoo Test and a small authorised sample, then review differences before applying any authorised adjustment. Importing counts and applying stock adjustments remain separate actions.

## Reference material

Reviewed on 2026-10-20 as general workflow references, not evidence of the client's database version:

- [Odoo 19 inventory adjustments](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/warehouses_storage/inventory_management/count_products.html).
- [Odoo 19 export and import data](https://www.odoo.com/documentation/19.0/applications/general/export_import_data.html).
- [Odoo issue 146595](https://github.com/odoo/odoo/issues/146595), historical report of counted quantities accumulating during import without the existing inventory record External ID; used to inform the update-by-record-ID approach, not as evidence of a current client defect.

Online search excerpts were available; direct fetching of the inventory and import documentation timed out. The supplied screenshot remains in the chat attachment. The builder and visual previews are in `Working Files/Stocktake Template/`.
