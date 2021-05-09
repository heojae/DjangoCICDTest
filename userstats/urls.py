from django.urls import path

from userstats.views import ExpenseSummaryStats, IncomeSummaryStats

urlpatterns = [
    path('expense_category_data/', ExpenseSummaryStats.as_view(), name="expense-summary-stat"),
    path('income_category_data/', IncomeSummaryStats.as_view(), name="income-summary-stat"),

]
