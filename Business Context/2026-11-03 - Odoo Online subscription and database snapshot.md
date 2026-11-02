# Odoo Online subscription and database snapshot

**Recorded:** 2026-11-03 (Australia/Perth). **Source:** subscription/database screenshot supplied by Veer in the inventory valuation chat, attachment `codex-clipboard-8ef6a185-74a0-440c-b6d5-623b5e53ca24.png`. Veer described this as the client's current plan and subscription and asked for useful information to be retained. This is a dated screenshot transcription, not an independent live-system or contract review.

The attachment includes a licence key. The key is deliberately omitted and the unredacted screenshot has not been copied into this repository. The original attachment remains the source evidence. No subscription, billing, database or configuration action was taken.

## Database and hosting

| Item | As shown or confirmed |
| --- | --- |
| Client/company context | UK Central Wholesale |
| Hosting platform | Odoo Online, confirmed by Veer |
| Database address | https://uk-central-wholesale.odoo.com/ |
| Version | **saas-19.4** |
| Production hosting region | Oceania |
| Backup hosting regions | Europe and Canada |

The version is the key correction to the preceding investigation: this database is shown on **saas-19.4**, not Odoo 20. Use the matching Odoo Online release context for further work. This evidence establishes the displayed version on the date supplied; it does not establish the version on every earlier date or guarantee that it remains unchanged after an upgrade.

## Subscription and displayed amounts

| Item | As shown |
| --- | --- |
| Current plan | Custom, marked Running |
| Subscription frequency | Yearly Subscription |
| Expiry | 3 September 2027 |
| Licensed users shown | 3 Users |
| Custom plan line | AUD 2,880.00 |
| Custom Plan First Year Discount — 3 Users | AUD −576.00 |
| Extra Modules: Maintenance (per 100 Lines) — 1100 LoC | AUD 324.00 |
| Pricing Compensation — 1 PCE | AUD −353.52 |
| Subtotal | AUD 2,274.48 |
| VAT (screen label) | AUD 227.45 |
| Total | AUD 2,501.93 |

The Custom card lists **All apps, Studio, API / Multi Company** and displays **AUD 80.00/user/month**. These are displayed plan features and a plan-card rate; they do not prove that Studio customisations, integrations or multiple companies are actually configured. Three licensed users does not establish the identities or number of active user accounts. The amount summary is not proof of payment, invoice status or a future renewal quote. The first-year discount and pricing compensation must not be assumed to recur.

The maintenance line records a billed **1100 LoC** quantity, but does not identify modules, their purpose, deployment mechanism or the scope of maintenance. It does not establish Odoo.sh hosting or permission to deploy custom server modules. Retain Odoo Online as the hosting baseline. The tax label is transcribed as VAT; it is not evidence of the client's configured GST reporting basis.

## Odoo contact and invoicing details

The screen labels **Derek Stewart (deste)** as the Odoo contact, with phone **+61 426 492 811** and email **deste@odoo.com**. This is the displayed Odoo contact, separate from Nitin as the primary client contact and Veer as the sole person responsible for this engagement.

The invoicing address shown is **On Point Uniforms, Perth, Australia**, although the database/company context is UK Central Wholesale. Confirm whether that billing entity is intentional when reviewing subscription administration. Do not infer a legal relationship, ownership, incorrect billing or the entity named on actual invoices from this screen alone.

## Available controls and limits shown

The page displays Renew, Add Users, Edit Address, View Invoices, Rename, Duplicate, Download Backup and View Admin Activity Logs controls. Their presence is useful for future administration or test planning, but does not establish that a duplicate/backup has been created, that an action will succeed with current permissions, or that Veer has standing authority or obligations to perform it.

Email usage is shown as **Today: 3/200 mail sent**, with a note that the limit will increase based on usage over time. This is a transient displayed counter, not a permanently guaranteed sending allowance. Backup frequency, retention, recovery objectives and contractual SLA terms are not established by this screenshot.

## Related record

- [Inventory valuation investigation and version correction](../Support%20Requests%20%26%20Outcomes/2026-11-02%20-%20Inventory%20valuation%20journal%20investigation.md).
