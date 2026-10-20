# Availability means on-hand minus reservations in the company's warehouse.
ribbon = env['product.ribbon'].with_context(lang='en_US').search([('name', '=ilike', 'Out of stock')])
if len(ribbon) != 1:
    raise UserError('Exactly one Out of stock ribbon is required.')
warehouses = env['stock.warehouse'].search([('company_id', '=', env.company.id)])
if len(warehouses) != 1:
    raise UserError('Select an explicit website warehouse before using this action with multiple warehouses.')
products = env['product.template'].with_context(warehouse_id=warehouses.id).search([('sale_ok', '=', True)])
to_tag = products.filtered(lambda p: p.is_storable and p.free_qty <= 0 and p.website_ribbon_id != ribbon)
to_clear = products.filtered(lambda p: p.website_ribbon_id == ribbon and (not p.is_storable or p.free_qty > 0))
if to_tag:
    to_tag.write({'website_ribbon_id': ribbon.id})
if to_clear:
    to_clear.write({'website_ribbon_id': False})
