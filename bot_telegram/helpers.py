from telethon.sync import Button


class ButtonsManager(object):

    def __init__(self):
        self.button = Button

    def get_start_button(self):
        return [
            [self.button.text("🌎 TK Global Technology", resize=True)]
        ]

    def get_expected_colors_buttons(self):
        return [
            [self.button.inline("🔴", "red_button"),
             self.button.inline("⚫", "black_button"),
             self.button.inline("⚪", "white_button")],
        ]

    def get_menu_buttons(self):
        return [
            [self.button.text("🆔 ID produto", resize=True)],
            [self.button.text("📧 E-mail", resize=True)],
            [self.button.text("⚙️ Configurar", resize=True),
             self.button.text("✅ TK GLobal", resize=True)],
        ]

    def get_account_buttons(self, data):
        return [
            [self.button.inline(f"E-mail = {data['user']['email']}", "email")],
            [self.button.inline(f"ID do contrato = {data['user']['product_id']}", "product_id")],
            [self.button.inline(f" Validar ✅", "confirmar"), self.button.inline(f"Voltar ➡", "voltar")]
        ]

    def get_more_buttons(self, data):
        return [
            [self.button.inline(f"Tipo de Conta = {data['settings']['account_type']}", "account_type")],
            [self.button.inline(f"Tipo de Entrada = {data['settings']['enter_type']}", "enter_type")],
            [self.button.inline(f"Valor Entrada = {data['settings']['enter_value']}", "enter_value")],
            [self.button.inline(f"Tipo de Stop = {data['settings']['stop_type']}", "stop_type")],
            [self.button.inline(f"Stop Gain = {data['settings']['stop_gain']}", "stop_gain")],
            [self.button.inline(f"Stop Loss = {data['settings']['stop_loss']}", "stop_loss")],
            [self.button.inline(f"Proteção no Branco = {data['settings']['protection_hand']}", "protection_hand")],
            [self.button.inline(f"Valor Proteção = {data['settings']['protection_value']}", "protection_value")],
            [self.button.inline(f"Martingale = {data['settings']['martingale']}", "martingale")],
            [self.button.inline(f"Martingale Branco = {data['settings']['white_martingale']}", "white_martingale")],
            [self.button.inline(f"Multiplicador Gale = {data['settings']['martingale_multiplier']}",
                                "martingale_multiplier")],
            [self.button.inline(f"Multiplicador Branco = {data['settings']['white_multiplier']}", "white_multiplier")],
            
            [self.button.inline(f"Gerenciamento TK = {data['settings']['white_gerenciamento_tk']}", "white_gerenciamento_tk")],
            [self.button.inline(f"Quantidade de entradas = {data['settings']['gerenciamento_tk_qtd']}", "gerenciamento_tk_qtd")],
            [self.button.inline(f"Reiniciar após wins = {data['settings']['gerenciamento_tk_qtd_win']}", "gerenciamento_tk_qtd_win")],
            [self.button.inline(f"Reiniciar após loss = {data['settings']['gerenciamento_tk_qtd_loss']}", "gerenciamento_tk_qtd_loss")],

            [self.button.inline(f"⬅", "previous"), self.button.inline(f"✅", "more_confirm"),
             self.button.inline(f"➡", "next")],
        ]

    def get_strategy_buttons(self, data):
        items_list = [
            [self.button.inline(f'{strategy["color"]} = {strategy["sequence"]}')
             for strategy in data["strategies"]][i:i + 1] + [self.button.inline(f"❌", f"delete_sequence_{i}")]
            for i in range(0, len(data["strategies"]), 1)
        ] if data.get("strategies") else []
        buttons_list = [
            [self.button.inline(f"➕", "new_item")],
            [self.button.inline(f"⬅", "back"), self.button.inline(f"✅", "new_confirm")]
        ]
        return items_list + buttons_list


Buttons = ButtonsManager()
