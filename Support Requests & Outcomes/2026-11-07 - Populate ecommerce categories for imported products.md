# Populate ecommerce categories for imported products

Veer requested on 7 November 2026 (Australia/Perth) that the missing Website Product Category column be populated for reimport. He authorised inferring ecommerce categories from the corresponding product categories and asked that uncertainties be raised.

Sources supplied in `C:/Users/veerm/Downloads/`:
- `Product (product.template) (4).xlsx`: 128 products, all website category cells blank.
- `Website Product Category (product.public.category).xlsx`: 29 existing website categories, including display names and identifiers.
- `Product Category (product.category) (6).xlsx`: 32 existing internal categories.

The prepared workbook is `Output/outputs/ecommerce-category-mapping-2026-11-07/Products - ecommerce categories populated.xlsx`. Each product's internal category was verified against the supplied category export. Removing the leading `UK Central Wholesale / ` produced exactly one existing website category display-name match for every product. One corresponding category was assigned per product. Additional cross-listing was not inferred.

| Website category | Products |
| --- | ---: |
| Chocolate & Confectionery / Chocolate Bars | 30 |
| Chocolate & Confectionery / Gifting | 64 |
| Chocolate & Confectionery / Childrens Confectionery | 3 |
| Crisps, Snacks & Biscuits / Biscuits Crackers and Cakes | 11 |
| Crisps, Snacks & Biscuits / UK Crisps and Snacks | 7 |
| Drinks / Soft Carbonated Drinks | 1 |
| Pack Formats / Hanging Bags | 6 |
| Pick & Mix and Bulk Sweets / Pick N Mix | 4 |
| Pick & Mix and Bulk Sweets / Walkers Nonsuch Toffee | 2 |
| Total | 128 |

Validation: all 128 saved assignments match the supplied website category paths. Cell-by-cell comparison confirmed only H2:H129 changed. Other values, cell formatting, sheet names, dimensions, freeze panes and merged ranges were preserved. Representative before/after ranges were rendered and visually reviewed. Original source files were not edited.

No ambiguous category matches were found under Veer's stated matching assumption. The product export contains neither External ID nor database ID. Before an update import, Veer needs to export the existing products with External IDs and join them to the prepared values, verifying the product matches. Do not invent product IDs or treat the internal reference as an Odoo update identifier. Odoo documents the role of External IDs in updates in its [import/export guidance](https://www.odoo.com/documentation/19.0/applications/general/export_import_data.html).

Status: workbook prepared for Veer. No live Odoo changes, import testing, import completion or client acceptance have been recorded. Pending: add verified product identifiers, map only the intended category update fields and identifier, then test and perform the import in Odoo.

## Follow-up: minimal update import

Veer added `Control Policy` to the populated workbook, with `purchase` on all 128 products. He then supplied `C:/Users/veerm/Downloads/Product (product.template) (5).xlsx` with the products' External IDs and requested an Excel file containing only the fields needed for the category and control policy update.

Prepared `Output/outputs/ecommerce-category-mapping-2026-11-07/Products - ecommerce and control policy import.xlsx` with one sheet and three columns: `External ID`, `Website Product Category/External ID`, and `Control Policy`. All 128 products matched uniquely by internal reference and exact product name. Product External IDs were copied from the new export. Category External IDs were matched uniquely from the supplied website category export. Control policy values were preserved as `purchase`.

The saved file was independently checked for exactly 128 rows of products and three columns, unique and complete product IDs, valid category IDs, and preserved control policy values. Its opening range was rendered and visually reviewed. No live import was performed. Pending: Veer to verify field mapping, test and perform the import in Odoo. This resolves the earlier missing-identifier issue.
