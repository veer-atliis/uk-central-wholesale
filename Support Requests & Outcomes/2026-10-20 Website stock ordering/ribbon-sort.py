# Always refresh availability ribbons before sorting, including manual runs.
sync = env['ir.cron'].with_context(active_test=False).search([('name', '=', 'Website: sync Out of stock ribbon (free stock)')])
if len(sync) != 1:
    raise UserError('Exactly one free-stock ribbon update action is required.')
sync.ir_actions_server_id.run()
# Use the English ribbon name; stock quantities do not affect this ordering.
ribbons = env['product.ribbon'].with_context(lang='en_US').search([('name', '=ilike', 'Out of stock')])
if not ribbons:
    raise UserError('The Out of stock ribbon was not found. No sequences were changed.')
products = env['product.template'].with_context(lang='en_US').search([('sale_ok', '=', True)])
products = products.sorted(key=lambda p: ((p.name or '').lower(), p.id))
first = []
last = []
for p in products:
    if p.website_ribbon_id in ribbons:
        last.append(p)
    else:
        first.append(p)
changed = 0
for seq, p in enumerate(first + last, start=1):
    if p.website_sequence != seq:
        p.write({'website_sequence': seq})
        changed += 1
