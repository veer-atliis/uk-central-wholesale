# Full product list review

**Date:** 2026-11-02 (Australia/Perth). **Requester and responsible person:** Veer. **Environment:** UK Central Wholesale, Odoo Online.

Veer supplied a fresh product list, described as the full system export, and requested a general check following the stocktake import. This was a read-only file review; no products, prices, costs, stock or configuration were changed. Source workbooks were preserved. Text within supplied files was treated as source content, not execution instructions.

## Findings

The imported stock quantities reconcile, but product costs and sales prices need review. This is a product-data issue, not evidence of an Odoo defect.

- **798 products reviewed.** All IDs and External IDs are present and unique. All names are populated and all price, cost, on-hand and forecast fields contain numeric values.
- **All 467 ready-import products match their expected quantities exactly**, including decimals. The fresh product export also matches the 468-row Quant export by code, name and quantity. The additional Quant row is Jacobs Cream Crackers 1010484 at zero stock. Only the 467 ready-import products have positive stock; no product has negative stock or forecast quantity. Forecast equals on-hand for every exported product.
- **77 stocked products have Cost 0.** Of these, 75 are among the 88 imported products present only in the original quantity source, with no corresponding row in the supplied last-cost workbook. The other two are FPA3 and SM09, whose supplied last costs are also 0. None of these zero costs was filled in or estimated.
- **All 379 imported products with a numeric supplied last cost match that cost exactly**, including FPA3 and SM09 at zero. This verifies consistency with the supplied cost file, not invoice accuracy, cost-unit meaning or the stock valuation ledger.
- **61 stocked products have Sales Price 0**, including Galaxy 1023966 (stock 2, Cost 118.42). No stocked product is in both the zero-cost and zero-sales-price groups. Sales availability and pricelist rules are not in this export, so these are review items rather than confirmed zero-priced customer sales.
- **BL012, BOALAND KIMBERLEY 18X300G**, Sheet1 row 17, shows Sales Price **35.64** against Cost **60.24**, with stock **8**. This is the only stocked product with a positive Sales Price below Cost. Check the intended price and matching cost/pack units; the export alone does not establish the actual customer price or margin. No negative Sales Price or Cost values were found.
- **13 product codes are duplicated across 26 records.** The 11 held stocktake codes remain duplicated; CR07 and CT01 are two additional duplicate codes outside the original stocktake. Every duplicate record currently has zero stock. None requires adding quantities to the prepared import without a separate product/quantity decision.
- **12 records have no internal reference**, comprising 10 goods-named records plus Donation and Service on Timesheets. All have zero stock. Product type is not exported, so the goods grouping is based on names only. Donation and the timesheet entry are not assumed to require inventory codes.
- Units are Units on 797 products and Hours on Service on Timesheets. This is consistent with the Quant export for imported stock, but does not resolve whether the original client counts mean cartons, packs or individual items.

## Comparison with the historical product export

All 797 historical template IDs remain present. Galaxy 2446 is the only additional ID. Existing references, names and External IDs match the historical snapshot exactly; 315 existing product Cost values differ. This is consistent with Veer's reported cost update, without establishing who changed each record or when. The 12 blank-reference records already existed in the historical export and are not newly created by the stock import. The export does not show archived records, filters or company context; its coverage is user-reported as full, not independently established against the database.

The historical export remains unchanged. This fresh export is the latest supplied product evidence as at the date above. Its IDs identify product templates, not product variants or stock.quant records.

## Suggested follow-up

1. Obtain the correct costs for the 77 stocked products below and confirm that each cost uses the same unit as the corresponding stock count. The available last-cost file does not supply non-zero replacement costs for them.
2. Review the 61 zero Sales Price records and BL012's Sales Price below Cost. Confirm whether pricing is intentionally supplied elsewhere, such as a pricelist, and check cost/pack units before deciding which product prices need changing.
3. Complete the existing client review for the 11 held stocktake codes. Record CR07 and CT01 as additional product-list duplication outside that quantity scope. Do not infer which duplicate is correct from its current cost or name suffix.
4. Add appropriate codes to the 10 goods-named blank-reference records if Veer confirms they are in use. Do not guess codes or alter Donation or Service on Timesheets by default.

This export does not include costing methods, valuation layers, stock movements, accounting entries, taxes, currencies, sales availability, inventory tracking settings, locations, variant detail or pricelist rules. No inventory value or margin conclusion is drawn from Cost alone. Odoo documentation explains that pricing rules can override the product Sales Price and that Cost and valuation behaviour depend on costing configuration. These are general references, not confirmation of the client's version or settings:

- [Odoo pricelists](https://www.odoo.com/documentation/19.0/applications/sales/sales/products_prices/prices/pricing.html).
- [Odoo stock-movement valuation](https://www.odoo.com/documentation/19.0/applications/inventory_and_mrp/inventory/inventory_valuation/operations_valuation.html).

## Stocked products with zero cost

Rows refer to Sheet1 of the fresh product export. Quantities are preserved as exported. Cost is 0 on all rows below.

| Row | Product code | Product name | Quantity on hand |
| --- | --- | --- | --- |
| 31 | BB13 | Barratt Bassetti Hard Liquorice Sticks 75s | 1 |
| 68 | CK11 | Bolands Chocolate Kimberly 20x132g | 8 |
| 70 | FR11 | Bolands Fig Rolls 24x200g | 17 |
| 78 | BP360 | Branston Piccalilli 6x360g | 1 |
| 87 | TO10 | Britvic Tango Orange Cans 24x330ml | 1 |
| 114 | 161860 | Cadbury Buttons Milk Chocolate 18x(4x14.4g) | 8 |
| 119 | CWS85 | Cadbury Curly Wurly Squirlies 10x85g | 25 |
| 124 | DMC120 | Cadbury Dairy Milk Caramel 16x120g | 26 |
| 130 | KD254 | Cadbury Dairy Milk Kids Bar 25x4pk | 12 |
| 131 | MEB54 | Cadbury Dairy Milk Mini Eggs Bar 48x54g - NEW PRODUCT | 50 |
| 134 | DD023 | Cadbury Double Decker 48x54.5g | 6 |
| 138 | FC16 | Cadbury Frys Chocolate Cream 16x3pk (48 units x 45g full size bar) | 20 |
| 139 | FO16 | Cadbury Frys Orange Cream 16x3pk (48 units x 45g full size) | 24 |
| 140 | FP163 | Cadbury Frys Peppermint Cream 16x3pk (48 units x 45g full size bar) | 24 |
| 141 | FT02 | Cadbury Frys Turkish Delight 24x3pk (72 units) | 13 |
| 156 | WI03 | Cadbury Wispa 11x4pk (98.4g) | 29 |
| 168 | CCSL90 | Chupa Chups Strawberry Laces 18x90g | 17 |
| 227 | HO10 | Halls Extra Strong Menthol Action Sweets 20x33.5g | 1 |
| 228 | WM01 | Hannah's White Choc Mice 12x140g | 10 |
| 232 | HRC140 | Haribo Rhubarb & Custard (Soft Rolls) 12x140g NEW PRODUCT | 33 |
| 239 | MC33 | Jacobs CRINKLEYS CHEESE & ONION 12x6pk | 10 |
| 243 | MC30 | Jacobs MINI CHEDDARS ORIGINAL 12x6pk | 20 |
| 245 | MC31 | Jacobs MINI CHEDDARS RED LEICESTER 12x6pk | 2 |
| 263 | BR10 | KINGSWAY BLACKBERRY & RASPBERRY BERRIES  3kg BAG (HUNDREDS/THOUSANDS) | 5 |
| 266 | KW08 | KINGSWAY BON BONS - BUBBLEGUM 3kg BAG | 20 |
| 267 | KW06 | KINGSWAY BON BONS - LEMON 3kg BAG | 3 |
| 272 | BB02 | KINGSWAY BUMBER BANANA 2kg BAG | 2 |
| 287 | FPA3 | KINGSWAY FIZZY PINEAPPLES 3KG | 6 |
| 309 | LC01 | KINGSWAY LIQUORICE CREAM ROCK 3kg BOX | 1 |
| 311 | MI05 | KINGSWAY MINT IMPERIALS 3kg BAG | 1 |
| 318 | SM09 | KINGSWAY SPACE MIX 3kg BAG | 1 |
| 325 | SF10 | KINGSWAY SUGAR FREE COLA BOTTLES 3x1kg BAGS IN BOX | 8 |
| 336 | DI02 | KP Snacks DISCOS CHEESE & ONION 28x50g - The BIG Bag | 10 |
| 338 | DI04 | KP Snacks DISCOS SALT & VINEGAR 28x50g - The BIG Bag | 10 |
| 342 | BHSV45 | KP Snacks HULA HOOPS "BIG HOOPS" SALT & VINEGAR 36x45g - NEW PACK SIZE | 20 |
| 343 | HH08 | KP Snacks HULA HOOPS BBQ BEEF 32x34g | 20 |
| 344 | BHO45 | KP Snacks HULA HOOPS BIG HOOPS ORIGINAL 36x45g - NEW PACK SIZE | 30 |
| 345 | HH11 | KP Snacks HULA HOOPS CHEESE & ONION 32x34g | 20 |
| 347 | HH03 | KP Snacks HULA HOOPS ORIGINAL 32x34g | 13 |
| 359 | KMPD170 | Kendal & Miller Pear Drops 12x170g | 20 |
| 360 | KMPC170 | Kendal & Miller Pineapple Cubes 12x170g - NEW | 1 |
| 400 | LT01 | Lion Liquorice Gums 2kg BOX | 3 |
| 404 | PB02 | Lion Poor Bens 2kg BOX | 1 |
| 425 | GB24 | Mars Galaxy Cookie Crumble 24x114g | 12 |
| 432 | MI09 | Mars Galaxy Minstrels 12x(3x42g) - splittable - 36x full size 42g bags | 24 |
| 492 | LA10110 | Maynards Bassetts Liquorice Allsorts 10x110g NEW PACK SIZE | 1 |
| 511 | OD350 | McDonnells Original Curry Sauce Squeezy Bottle 12x350g - NEW PRODUCT | 20 |
| 516 | MB300 | McVities Bourbon Creams 12x300g PM 135 | 30 |
| 539 | CM01 | Millions Cola Tubes 12x60g | 3 |
| 543 | MOB1 | Miwadi Miwadi Blackcurrant Cordial 12x1ltr | 6 |
| 544 | MOC1 | Miwadi Miwadi Orange Cordial 12x1ltr | 12 |
| 555 | LB11 | Nestle Lion Bar 10x4pk (120g) | 12 |
| 566 | SM12 | Nestle Smarties Tubes 16x3pk | 10 |
| 576 | VI14 | Nichols PLC Vimto Cordial No Added Sugar 12x725ml | 2 |
| 614 | PW02 | Real Candy Co Pink & White Nougat 16x130g | 1 |
| 623 | RA33 | Robinsons Apple & Blackcurrant NAS Double Concentrate 12x1ltr | 2 |
| 635 | RA21 | Robinsons Peach NAS Fruit & Barley 12x1ltr | 2 |
| 663 | SCC3 | STOCKLEYS COLA CUBES 3kg - NEW PRODUCT | 3 |
| 690 | WA25 | Smiths BACON FRIES 48x24g | 15.5 |
| 691 | WA19 | Smiths SCAMPI FRIES 48x27g | 9 |
| 694 | SB138 | Starburst Original Chews 12x138g | 16 |
| 700 | GF01 | Swizzels Giant Fizzers 24pk | 3 |
| 707 | SQCC140 | Swizzels Squashies Cherry Cola 12x140g - NEW PRODUCT | 20 |
| 715 | SQT100 | Swizzels Squashies Tropical 12x100g - NEW | 5 |
| 742 | WCO45 | Walkers CHEESE & ONION 32x45g | 20 |
| 746 | MM33 | Walkers MONSTER MUNCH ROAST BEEF 18x6pk | 4 |
| 747 | MM29 | Walkers MONSTER MUNCH ROAST BEEF 35x40g | 20 |
| 748 | MM28 | Walkers MONSTER MUNCH SWEET & SPICY (Previously Flamin' Hot) 35x40g | 20 |
| 755 | CE08 | Walkers Nonsuch English Creamy Toffee 12x150g | 3 |
| 760 | WM02 | Walkers Nonsuch Mint Toffee Bags 12x150g | 5 |
| 762 | WT02 | Walkers Nonsuch Original Toffee Tray 10x100g | 1 |
| 771 | WPC45 | Walkers PRAWN COCKTAIL 32x45g | 20 |
| 776 | WRC45 | Walkers ROAST CHICKEN 32x45g | 10 |
| 778 | WSV45 | Walkers SALT & VINEGAR 32x45g | 10 |
| 780 | WSB45 | Walkers SMOKY BACON 32x45g | 10 |
| 784 | WOT36 | Walkers WOTSITS CHEESE 30x36g - NEW BIGGER BAG | 30 |
| 797 | ZLF800 | Zoflora Linen Fresh Trigger Spray 8x800ml - NEW PRODUCT | 1 |

## Stocked products with zero Sales Price

Sales Price is 0 on all rows below. Cost is shown for identification and review, not as a recommended selling price.

| Row | Product code | Product name | Quantity on hand | Cost |
| --- | --- | --- | --- | --- |
| 2 | 1023966 | **GALAXY BLOCK 17X360G | 2 | 118.42 |
| 4 | 578329 | ARIEL LIQ ORIGINAL 43W 4X1.33L | 4 | 40.59 |
| 5 | 572687 | ARIEL PLAT FEBREZE PODS 3X50S | 4 | 57.5 |
| 6 | 572653 | ARIEL PLAT STAIN PODS 3X50S | 4 | 57.5 |
| 7 | 547929 | ARIEL STAIN GEL COLOUR 6X800ML | 4 | 33.35 |
| 8 | 547953 | ARIEL STAIN GEL WHITE 6X800ML | 4 | 33.35 |
| 18 | 540460 | BOLD 3IN1 PODS SPRING 4X13CT | 4 | 23.03 |
| 19 | 584201 | BOLD LIQ LAV/CHAM 57W 4X1.767L | 4 | 52.69 |
| 20 | 580897 | BOLD PODS SPRING AWAK 3X60CT | 4 | 65.62 |
| 96 | 481888 | CIF ALL PURP CLEAN LEMON 2X5L | 4 | 18.42 |
| 97 | 481896 | CIF GLASS/MULTI SPRAY 6X750ML | 4 | 18.42 |
| 98 | 561218 | CIF MULTI SPRAY AURORA 6X750ML | 4 | 16.44 |
| 99 | 481903 | CIF SPRAY STAINLESS 6X750ML | 4 | 18.42 |
| 100 | 481870 | CIF WASHROOM SPRAY 6X750ML | 4 | 18.42 |
| 101 | 581537 | COMFORT CREAT COTSWOLD 6X1.4L | 4 | 27.42 |
| 102 | 545791 | COMFORT F/CON PURE 31W 8X930ML | 4 | 26.32 |
| 103 | 545783 | COMFORT F/CON SUNSHINY 8X930ML | 4 | 26.32 |
| 192 | ER060 | Erin Meal Time Irish Country Stew Mix 24x39g - NEW PRODUCT | 14 | 38.18 |
| 194 | 558695 | FEBREZE COTTON FRESH 8X500ML | 4 | 39.72 |
| 195 | 558736 | FEBREZE FRESH LINEN 8X500ML | 4 | 39.72 |
| 196 | 558687 | FEBREZE PET FRESH 8X500ML | 4 | 39.72 |
| 197 | 571259 | FEBREZE SPRING AWAKEN 8X500ML | 4 | 39.72 |
| 198 | 558679 | FEBREZE UNSTOPPABLE 8X500ML | 4 | 43.23 |
| 199 | 540329 | FLASH LIQ ALL PURP LEMON 6X1L | 4 | 19.74 |
| 200 | 540337 | FLASH LIQ ALL PURP PET 6X1L | 4 | 19.74 |
| 201 | 540353 | FLASH LIQ ALL PURP WOOD 6X1L | 4 | 19.74 |
| 202 | 540428 | FLASH LIQ APPLE BLOSSOM 6X1L | 4 | 19.74 |
| 203 | 459158 | FLASH SPRAY BATHROOM 10X800ML | 4 | 41.69 |
| 204 | 459132 | FLASH SPRAY BLEACH 10X800ML | 4 | 41.69 |
| 205 | 457277 | FLASH SPRAY KITCHEN 10X800ML | 4 | 41.69 |
| 315 | KSL3 | KINGSWAY SHERBET LEMONS 3kg - NEW PRODUCT | 13 | 23.06 |
| 366 | 449084 | LENOR CREASE EXOTIC 5X500ML | 4 | 21.93 |
| 368 | 490871 | LENOR CREASE RUBY JAS 5X500ML | 4 | 21.93 |
| 370 | 577512 | LENOR F/CON COASTAL 6X1.488L | 4 | 36.86 |
| 371 | 577520 | LENOR F/CON EXOTIC AMB 6X1.49L | 2 | 36.86 |
| 372 | 577570 | LENOR F/CON GOLD ORCH 6X1.49L | 4 | 36.86 |
| 373 | 577538 | LENOR F/CON JASMINE 6X1.488L | 2 | 36.86 |
| 374 | 498271 | LENOR F/CON OCEAN MIST 6X1.65L | 4 | 27.42 |
| 375 | 517328 | LENOR F/CON SPRING 43W 6X1.42L | 12 | 23.03 |
| 376 | 580945 | LENOR F/CON SUMMER 43W 6X1.42L | 4 | 25.23 |
| 377 | 490920 | LENOR IRON WATER SPRING 6X1L | 4 | 12.93 |
| 378 | 490805 | LENOR IRON WATER SUMMER 6X1L | 4 | 12.93 |
| 379 | 577463 | LENOR OUTDOOR 1ST SPRING 8X630 | 4 | 34.23 |
| 380 | 570780 | LENOR OUTDOOR CAPRI 8X742ML | 4 | 34.23 |
| 381 | 577653 | LENOR OUTDOOR CORFU 8X700ML | 4 | 48.28 |
| 382 | 540527 | LENOR OUTDOOR N/SOLST 8X630ML | 4 | 34.23 |
| 383 | 577679 | LENOR OUTDOOR SANTORINI 8X700 | 4 | 48.28 |
| 589 | 579369 | PERSIL CAPSULES BIO 3X34S | 4 | 39.5 |
| 590 | 579377 | PERSIL CAPSULES COLOUR 3X34S | 4 | 39.5 |
| 591 | 579385 | PERSIL CAPSULES NON BIO 3X34S | 4 | 39.5 |
| 592 | 558645 | PERSIL ULT LIQ ACTIVE 5X1.24L | 4 | 47.2 |
| 593 | 544024 | PERSIL ULT LIQ COMFORT 5X1.24L | 4 | 47.2 |
| 594 | 578505 | PERSIL ULT LIQ FRESH 6X837ML | 4 | 39.5 |
| 598 | PP01 | Paynes Mint Cream Poppets 36x40g | 6 | 34.05 |
| 670 | SPD3 | STOCKLEYS PEAR DROPS 3kg - NEW PRODUCT | 20 | 27.85 |
| 672 | 317610 | STOCKLEYS PINEAPPLE CUBES 3kg - NEW PRODUCT | 20 | 28.52 |
| 674 | SRA3 | STOCKLEYS ROSY APPLES 3kg - NEW PRODUCT | 20 | 28.52 |
| 740 | 78161 | WALKERS OLDE ENG TOFFEE 2.5KG | 12 | 30.28 |
| 790 | 584345 | ZOFLORA COUNTRY GARDEN 12X120 | 10 | 28.98 |
| 791 | 572231 | ZOFLORA MANDARIN LIME 12X250ML | 10 | 43.89 |
| 792 | 568793 | ZOFLORA WINTER SPICE 12X500ML | 6 | 76.82 |

## Duplicate product codes

All records below have on-hand and forecast quantities of 0. Costs differ between some records and do not establish the correct product to count.

| Product code | Stocktake review | Rows | Template IDs | Names | Costs |
| --- | --- | --- | --- | --- | --- |
| BDT80 | Existing held item | 49, 50 | 1974, 2045 | Barrys Decaf Teabags 6x250g (80pk) / Barrys Decaf Teabags 6x250g (80pk) - NEW | 45.79 / 0 |
| BFH130 | Existing held item | 35, 36 | 867, 1040 | Barratt Flump Hearts 12x130g / Barratt Flump Hearts 12x130g - NEW PRODUCT | 0 / 0 |
| BFS120 | Existing held item | 38, 39 | 868, 869 | Barratt Fruit Salad Fruity Mix 12x120g - NEW PRODUCT / Barratt Fruit Salad Squishy Sunburst 12x120g | 0 / 0 |
| BT03 | Existing held item | 54, 55 | 2049, 1970 | Barrys Master Blend Teabags 6x250g (80pk) / Barrys Master Blend Teabags 6x250g (80pk) - NEW PRODUCT | 38.12 / 0 |
| CM05 | Existing held item | 145, 147 | 1861, 1212 | Cadbury Ireland Mint Crisp 48x54g / Cadbury Mint Crisp 48x49g (Irish Cadbury) | 103.12 / 0 |
| CO07S | Existing held item | 81, 82 | 2008, 1850 | Britvic Ireland Club Orange 24x330ml Slimline Can / Britvic Ireland Club Orange 24x330ml Slimline Can | 0 / 32.37 |
| CR07 | Outside original stocktake | 84, 85 | 1852, 2010 | Britvic Ireland Club Rock Shandy 8x1.75ltr Bottle / Britvic Ireland Club Rock Shandy 8x1.75ltr Bottle - NEW | 0 / 0 |
| CT01 | Outside original stocktake | 146, 152 | 1862, 1216 | Cadbury Ireland Tiffin 48x53g / Cadbury Tiffin 48x49g (Irish Cadbury) | 0 / 0 |
| EC03 | Existing held item | 644, 645 | 1035, 1411 | Ross's Edinbro' Castle Rock Sticks in Tartan Box 24x6pk / Ross's Edinbro' Castle Rock Sticks in Tartan Box 24x6pk | 0 / 67.92 |
| GC01 | Existing held item | 142, 144 | 1211, 1860 | Cadbury Golden Crisp 48x49g (Irish Cadbury) / Cadbury Ireland Golden Crisp 48x54g | 103.12 / 0 |
| LFG130 | Existing held item | 390, 391 | 895, 1673 | Lion Football Gums 12x130g / Lion Football Gums 12x130g BAG | 15.1 / 0 |
| LLG130 | Existing held item | 398, 399 | 898, 1678 | Lion Liquorice Gums 12x130g / Lion Liquorice Gums 12x130g BAG | 15.1 / 0 |
| LMG130 | Existing held item | 401, 403 | 1680, 899 | Lion Midget Gems 12x130g BAG / Lion Mini Gems 12x130g | 15.1 / 0 |

## Records without a product code

All have zero stock.

| Row | Template ID | Name | Unit |
| --- | --- | --- | --- |
| 94 | 2357 | CADBURY FLAKE 4PK 20X4X80G | Units |
| 95 | 2438 | CAPRI SUN ORANGE4X8PK | Units |
| 184 | 3 | Donation | Units |
| 186 | 2439 | ERIN IRISH COUNTRY STEW 24X39G | Units |
| 237 | 2435 | JACOBS MIKADO CHOC 18X176G | Units |
| 415 | 2355 | MILKYWAY MAGIC STARS 12X100G | Units |
| 514 | 2426 | McVITI JAMMY APPLE 18X136.5G | Units |
| 515 | 2425 | McVITIES JAMMY RASP 18X136.5G | Units |
| 588 | 2443 | PAYNES TOFFEE POPPETS 36x39g | Units |
| 671 | 2363 | STOCKLEYS PINEAPPLE CUBES 3KG | Units |
| 689 | 2352 | Service on Timesheets | Hours |
| 716 | 2430 | TERRYS MINT CRISP MINIS 10X80G | Units |

## Evidence and validation

- [Fresh full product export](../Go%20Live%20Files/Client%20Supplied/Product%20%28product.template%29%20%283%29.xlsx), Sheet1 A1:K799. Original supplied from Downloads, retained unchanged with matching SHA-256 `3a0462bee915eb92166637a99d0187b0c3bac773a0572f0f68ab600799f0bfc0`.
- [Prepared stock import](../Go%20Live%20Files/Edited/Stock%20Import/Stock%20Import%20-%20Ready.xlsx), Import A1:B468.
- [Post-import Quant export](../Go%20Live%20Files/Client%20Supplied/Quant%20%28stock.quant%29%20%281%29.xlsx), Sheet1 A1:G469.
- [Original quantity source](../Go%20Live%20Files/Client%20Supplied/UK_Central_Wholesale_-_Stocktake_1_Oct_2026.xlsx), Stocktake. This remains quantity authority.
- [Supplied last-cost context](../Go%20Live%20Files/Client%20Supplied/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx), Stocktake G, matched by column A. It is not quantity authority.
- [Historical product snapshot](../Go%20Live%20Files/Edited/UK_Central_Wholesale_Stocktake_with_Last_Cost.xlsx), Product ID & Cost A:E, compared by template database ID rather than row order.

Comparisons use stored values and exact decimal arithmetic without conversions or rounding. The raw Quant-to-product check covers names and quantities; the independent ready-file check covers all 467 expected code/quantity pairs. Category counts and complete exception records are retained in Working Files/2026-11-02 Stock Import/full-products-audit.json. The repeatable extraction and review script is audit-full-products.py in the same folder. Workbook formulas and error cells were checked separately; no workbook or live-system corrections were performed.
