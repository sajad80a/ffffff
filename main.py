from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from sympy import symbols, diff, integrate, sympify

# قاعدة بيانات مؤقتة لتخزين الحسابات والقروض
accounts = {}
loans = 0
budget = {'assets': 0, 'liabilities': 0, 'equity': 0}
ledger = []  # سجل القيود المحاسبية

# الوظائف المحاسبية
def add_account(account_type, value, increase):
    if account_type not in accounts:
        accounts[account_type] = 0
    if increase:
        accounts[account_type] += value
    else:
        accounts[account_type] -= value

def reset_accounts():
    global accounts
    accounts = {}

def calculate_net_profit():
    return budget['assets'] - budget['liabilities']

def add_entry(debit_account, credit_account, amount):
    # إضافة قيد محاسبي مزدوج
    ledger.append({'debit': debit_account, 'credit': credit_account, 'amount': amount})
    add_account(debit_account, amount, True)
    add_account(credit_account, amount, False)

# الحسابات الرياضية
def solve_equation(eq):
    try:
        result = eval(eq)
        return result
    except Exception as e:
        return f"Error: {e}"

def calculate_integral(equation):
    try:
        x = symbols('x')
        expr = sympify(equation)
        integral = integrate(expr, x)
        return integral
    except Exception as e:
        return f"Error: {e}"

def calculate_derivative(equation):
    try:
        x = symbols('x')
        expr = sympify(equation)
        derivative = diff(expr, x)
        return derivative
    except Exception as e:
        return f"Error: {e}"

# الشاشات المختلفة
class IntegralScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.equation_input = TextInput(hint_text="Enter equation for integration", multiline=False)
        self.result_label = Label(text="Integral Result will be shown here.")
        
        calculate_button = Button(text="Calculate Integral", on_press=self.calculate_integral)
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.equation_input)
        layout.add_widget(calculate_button)
        layout.add_widget(self.result_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def calculate_integral(self, instance):
        equation = self.equation_input.text
        result = calculate_integral(equation)
        self.result_label.text = f"Integral: {result}"

    def back_to_home(self, instance):
        self.manager.current = 'home'


class DerivativeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.equation_input = TextInput(hint_text="Enter equation for derivative", multiline=False)
        self.result_label = Label(text="Derivative Result will be shown here.")
        
        calculate_button = Button(text="Calculate Derivative", on_press=self.calculate_derivative)
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.equation_input)
        layout.add_widget(calculate_button)
        layout.add_widget(self.result_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def calculate_derivative(self, instance):
        equation = self.equation_input.text
        result = calculate_derivative(equation)
        self.result_label.text = f"Derivative: {result}"

    def back_to_home(self, instance):
        self.manager.current = 'home'


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        buttons = [
            ("Withdraw Loan", self.go_to_loan),
            ("Repay Loan", self.go_to_loan),
            ("View Accounts", self.go_to_accounts),
            ("View Budget", self.go_to_budget),
            ("Accounting Entries", self.go_to_accounting),
            ("Net Profit", self.go_to_profit),
            ("General Ledger", self.go_to_ledger),
            ("Trial Balance", self.go_to_trail_balance),
            ("Calculate Integral", self.go_to_integral),
            ("Calculate Derivative", self.go_to_derivative),
        ]

        for text, action in buttons:
            button = Button(text=text, on_press=action)
            layout.add_widget(button)

        self.add_widget(layout)

    def go_to_loan(self, instance):
        self.manager.current = 'loan'

    def go_to_accounts(self, instance):
        self.manager.current = 'accounts'

    def go_to_budget(self, instance):
        self.manager.current = 'budget'

    def go_to_accounting(self, instance):
        self.manager.current = 'accounting'

    def go_to_profit(self, instance):
        self.manager.current = 'profit'

    def go_to_ledger(self, instance):
        self.manager.current = 'ledger'

    def go_to_trail_balance(self, instance):
        self.manager.current = 'trail_balance'

    def go_to_integral(self, instance):
        self.manager.current = 'integral'

    def go_to_derivative(self, instance):
        self.manager.current = 'derivative'


class LoanScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.loan_input = TextInput(hint_text="Enter loan amount", multiline=False)
        layout.add_widget(self.loan_input)

        withdraw_button = Button(text="Withdraw Loan", on_press=self.withdraw_loan)
        repay_button = Button(text="Repay Loan", on_press=self.repay_loan)
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(withdraw_button)
        layout.add_widget(repay_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def withdraw_loan(self, instance):
        try:
            amount = float(self.loan_input.text)
            global loans
            loans += amount
            self.loan_input.text = ""
        except ValueError:
            self.loan_input.text = "Invalid amount"

    def repay_loan(self, instance):
        try:
            amount = float(self.loan_input.text)
            global loans
            loans -= amount
            self.loan_input.text = ""
        except ValueError:
            self.loan_input.text = "Invalid amount"

    def back_to_home(self, instance):
        self.manager.current = 'home'


class AccountsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.accounts_label = Label(text=str(accounts))
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.accounts_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'


class AccountingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.debit_input = TextInput(hint_text="Debit Account", multiline=False)
        self.credit_input = TextInput(hint_text="Credit Account", multiline=False)
        self.amount_input = TextInput(hint_text="Amount", multiline=False)

        add_entry_button = Button(text="Add Entry", on_press=self.add_entry)
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.debit_input)
        layout.add_widget(self.credit_input)
        layout.add_widget(self.amount_input)
        layout.add_widget(add_entry_button)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_entry(self, instance):
        try:
            debit_account = self.debit_input.text
            credit_account = self.credit_input.text
            amount = float(self.amount_input.text)

            if debit_account and credit_account and amount > 0:
                add_entry(debit_account, credit_account, amount)
                self.debit_input.text = ""
                self.credit_input.text = ""
                self.amount_input.text = ""
            else:
                raise ValueError("Invalid input")
        except ValueError:
            self.amount_input.text = "Error: Invalid input"

    def back_to_home(self, instance):
        self.manager.current = 'home'


class LedgerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.ledger_label = Label(text="General Ledger")
        self.ledger_text = Label(text=str(ledger))
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.ledger_label)
        layout.add_widget(self.ledger_text)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'


class BudgetScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.budget_label = Label(text=f"Assets: {budget['assets']}\nLiabilities: {budget['liabilities']}\nEquity: {budget['equity']}")
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.budget_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'


class ProfitScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.profit_label = Label(text=f"Net Profit: {calculate_net_profit()}")
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.profit_label)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'


class TrailBalanceScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.trail_balance_label = Label(text="Trial Balance")
        self.trail_balance_text = Label(text="Here you will see the trial balance details.")
        back_button = Button(text="Back", on_press=self.back_to_home)

        layout.add_widget(self.trail_balance_label)
        layout.add_widget(self.trail_balance_text)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'

# إدارة الشاشات
class AccountingApp(App):
    def build(self):
        self.manager = ScreenManager()

        self.manager.add_widget(HomeScreen(name='home'))
        self.manager.add_widget(LoanScreen(name='loan'))
        self.manager.add_widget(AccountsScreen(name='accounts'))
        self.manager.add_widget(AccountingScreen(name='accounting'))
        self.manager.add_widget(IntegralScreen(name='integral'))
        self.manager.add_widget(DerivativeScreen(name='derivative'))
        self.manager.add_widget(LedgerScreen(name='ledger'))
        self.manager.add_widget(BudgetScreen(name='budget'))
        self.manager.add_widget(ProfitScreen(name='profit'))
        self.manager.add_widget(TrailBalanceScreen(name='trail_balance'))

        return self.manager


if __name__ == '__main__':
    AccountingApp().run()
