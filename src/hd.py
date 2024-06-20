class HelpdeskRequired(models.Model):
    _inherit = "helpdesk.ticket"  # Hereda la clase "helpdesk.ticket" del modelo de datos existente.

    def write(self, vals):
        # Validar que tenga campos de base de conocimientos si pasa a etapa de cierre
        # interceptando la escritura del ticket.
        # _logger.warning("write:{}".format(vals))  #  Este código emite una advertencia con el contenido de los valores (vals) al escribir en el ticket.

        target_id = vals.get('stage_id') if 'stage_id' in vals.keys() else False  #  Obtiene el ID del nuevo estado del ticket si existe, de lo contrario, establece como falso.
        origin = self.stage_id if 'stage_id' in self else False  #  Obtiene el estado actual del ticket si existe, de lo contrario, establece como falso.
        if target_id:
            target = self.env['helpdesk.stage'].browse(target_id)  #  Busca el nuevo estado del ticket.
        is_close = target.is_close if target_id else self.stage_id.is_close  #  Verifica si el nuevo estado o el estado actual del ticket es de cierre.
        # _logger.warning("is_close:{}".format(is_close))  #  Este código emite una advertencia con el estado de cierre del ticket.

        if is_close:  #  Si el ticket está en un estado de cierre.
            has_product = vals.get('product_category') if 'product_category' in vals.keys() else \
                self.product_category if 'product_category' in self else False  #  Verifica si se ha proporcionado una categoría de producto para el ticket.
            if has_product:
                fields_missing = []
                # _logger.warning("has_product:{}".format(has_product))  #  Este código emite una advertencia si el ticket tiene una categoría de producto.

                ticket_type = vals.get('ticket_type_id') if 'ticket_type_id' in vals.keys() else \
                    self.ticket_type_id if 'ticket_type_id' in self else False  #  Verifica si se ha proporcionado un tipo de ticket.
                if not ticket_type:
                    fields_missing.append("Tipo de vale")  #  Agrega un campo faltante si el tipo de ticket no se ha proporcionado.

                report = vals.get('report') if 'report' in vals.keys() else \
                    self.report if 'report' in self else False  #  Verifica si se ha proporcionado un informe del cliente.
                if not report:
                    fields_missing.append("Reporte del cliente")  #  Agrega un campo faltante si el informe del cliente no se ha proporcionado.

                issue = vals.get('issue') if 'issue' in vals.keys() else \
                    self.issue if 'issue' in self else False  #  Verifica si se ha proporcionado un problema.
                if not issue:
                    fields_missing.append("Incidencia")  #  Agrega un campo faltante si el problema no se ha proporcionado.

                solution = vals.get('solution') if 'solution' in vals.keys() else \
                    self.solution if 'solution' in self else False  #  Verifica si se ha proporcionado una solución.
                if not solution:
                    fields_missing.append("Solución")  #  Agrega un campo faltante si la solución no se ha proporcionado.
                # _logger.warning("\n\nticket_type:{} report:{} issue:{} solution:{}".format(ticket_type, report, issue, solution))  #  Este código emite una advertencia con los detalles del ticket.

                fields_errors = "\n".join(fields_missing)  #  Une los campos faltantes en un solo mensaje.

                if fields_missing:
                    raise UserError("Al Ticket le falta:\n{}".format(fields_errors))  #  Si faltan campos requeridos, genera un error de usuario con los campos faltantes.
            # else:
            #     _logger.warning("SIN producto")  #  Este código emite una advertencia si no hay categoría de producto para el ticket.

        return super(HelpdeskRequired, self).write(vals)  #  Llama al método de escritura del modelo de datos principal con los valores proporcionados.
