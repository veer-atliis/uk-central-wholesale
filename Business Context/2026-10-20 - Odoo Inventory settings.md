# Odoo Inventory settings as at 20 October 2026

**Effective snapshot date: 2026-10-20 (Australia/Perth).** Veer supplied the screenshot as the client's current Inventory settings and asked for these settings to be retained for future AI chats. This is a dated baseline, not a guarantee that the configuration remains unchanged after this date.

**Environment:** UK Central Wholesale, Odoo Online. The Odoo version has not been confirmed.

**Evidence:** [Original settings screenshot](Sources/2026-10-20%20-%20Odoo%20Inventory%20settings.png), supplied by Veer on 2026-10-20. The values below are transcribed from the visible screen. No live database inspection or configuration changes were performed. Save and Discard buttons are visible; whether there were unsaved changes was not independently checked.

## Operations

| Setting | As shown on 2026-10-20 |
| --- | --- |
| Packages | Disabled |
| Batch, Wave & Cluster Transfers | Disabled |
| Partner-Specific Instructions | Enabled |
| Quality | Disabled |
| Allow Spontaneous Returns | Enabled |
| Spontaneous return period | 14 days after delivery |
| Shipping Policy | Visible text starts “As soon as possible, with”; remaining text is truncated, so the full selection is not confirmed |
| Annual Inventory Date | 31 December |

The annual inventory setting does not establish an agreed stocktake date for a particular year.

## Barcode

| Setting | As shown on 2026-10-20 |
| --- | --- |
| Barcode Scanner | Enabled |
| Stock Barcode Database | Disabled |
| Barcode Nomenclature | Default Nomenclature |
| Multiscan Separator | A value is present; exact punctuation has not been reliably transcribed. Refer to the screenshot if needed |
| RFID Timer | 1,000; the field does not show a unit beside the value |
| Mute Barcode application sounds | Disabled |
| Max time between each key | 150 ms, using the unit stated in the field description |

## Shipping

| Setting | As shown on 2026-10-20 |
| --- | --- |
| Delivery Methods | Enabled |
| Transport Management | Disabled |
| Confirmation Email | Disabled |
| Text Confirmation | Disabled |
| Signature | Disabled |

## Products, traceability and valuation

| Setting | As shown on 2026-10-20 |
| --- | --- |
| Variants | Enabled |
| Units of Measure & Packagings | Enabled |
| Lots & Serial Numbers | Disabled |
| Consignment | Disabled |
| Landed Costs | Enabled |
| Landed Costs — Default Journal | No value visible |

“Units of Measure & Packagings” and the separate “Packages” setting are different controls. The former is enabled and the latter disabled in this snapshot.

## Warehouse, scheduling and logistics

| Setting | As shown on 2026-10-20 |
| --- | --- |
| Storage Locations | Disabled |
| Multi-Step Routes | Disabled |
| Replenishment Horizon | 365 days |
| Days to Purchase | 0 days |
| Security Lead Time for Sales | Disabled |
| Dropshipping | Enabled |
| Replenish on Order (MTO) | Disabled |

## Implications for stocktake work

- Identify and count each product variant separately.
- Use the product's actual inventory unit of measure. The enabled units and packagings setting does not establish any particular carton conversion.
- This baseline does not require lot, serial, package or owner columns in the simple stocktake template.
- Disabled Storage Locations does not prove that no underlying stock location exists, or establish the number of warehouses. Verify the applicable stock record and location when preparing an import.
- Actual products, units, packaging conversions, stock locations, inventory record identifiers and import field mappings have not been established by this screenshot.

For future work, use this snapshot as the last documented baseline and confirm any configuration on which the task depends. Record later changes with their own dates and evidence, retaining this historical snapshot.
