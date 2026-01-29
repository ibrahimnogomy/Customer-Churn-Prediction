#!/usr/bin/env python3
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List


@dataclass
class CartItem:
    name: str
    price: float
    quantity: int = 1

    @property
    def total(self) -> float:
        return self.price * self.quantity


@dataclass
class CashierCart:
    items: Dict[str, CartItem] = field(default_factory=dict)
    discount_percent: float = 0.0
    tax_percent: float = 0.0

    def add_item(self, name: str, price: float, quantity: int = 1) -> None:
        key = name.strip().lower()
        if key in self.items:
            self.items[key].quantity += quantity
            self.items[key].price = price
        else:
            self.items[key] = CartItem(name=name.strip(), price=price, quantity=quantity)

    def remove_item(self, name: str) -> bool:
        key = name.strip().lower()
        return self.items.pop(key, None) is not None

    def update_quantity(self, name: str, quantity: int) -> bool:
        key = name.strip().lower()
        if key not in self.items:
            return False
        if quantity <= 0:
            self.items.pop(key, None)
        else:
            self.items[key].quantity = quantity
        return True

    def clear(self) -> None:
        self.items.clear()
        self.discount_percent = 0.0
        self.tax_percent = 0.0

    def subtotal(self) -> float:
        return sum(item.total for item in self.items.values())

    def discount_amount(self) -> float:
        return self.subtotal() * (self.discount_percent / 100)

    def tax_amount(self) -> float:
        return (self.subtotal() - self.discount_amount()) * (self.tax_percent / 100)

    def total_due(self) -> float:
        return self.subtotal() - self.discount_amount() + self.tax_amount()


def format_currency(value: float) -> str:
    return f"{value:,.2f}"


def print_header() -> None:
    print("=" * 50)
    print("نظام كاشير بسيط - تشغيل محلي")
    print("Simple Cashier System - Local Run")
    print("=" * 50)


def print_menu() -> None:
    print("\nاختر عملية / Choose action:")
    print("1) عرض السلة / View cart")
    print("2) إضافة صنف / Add item")
    print("3) تعديل الكمية / Update quantity")
    print("4) حذف صنف / Remove item")
    print("5) إضافة خصم % / Set discount %")
    print("6) إضافة ضريبة % / Set tax %")
    print("7) إنهاء وحفظ الفاتورة / Checkout & save")
    print("8) تفريغ السلة / Clear cart")
    print("0) خروج / Exit")


def print_cart(cart: CashierCart) -> None:
    if not cart.items:
        print("\nالسلة فارغة / Cart is empty.")
        return
    print("\nالسلة الحالية / Current cart:")
    print("-" * 50)
    for item in cart.items.values():
        print(
            f"{item.name} | Qty: {item.quantity} | Price: {format_currency(item.price)} | Total: {format_currency(item.total)}"
        )
    print("-" * 50)
    print(f"Subtotal: {format_currency(cart.subtotal())}")
    if cart.discount_percent:
        print(
            f"Discount ({cart.discount_percent:.1f}%): -{format_currency(cart.discount_amount())}"
        )
    if cart.tax_percent:
        print(f"Tax ({cart.tax_percent:.1f}%): +{format_currency(cart.tax_amount())}")
    print(f"Total Due: {format_currency(cart.total_due())}")


def prompt_float(message: str) -> float:
    while True:
        raw = input(message).strip()
        try:
            value = float(raw)
        except ValueError:
            print("⚠️  أدخل رقم صالح / Enter a valid number.")
            continue
        if value < 0:
            print("⚠️  الرقم يجب أن يكون موجب / Must be non-negative.")
            continue
        return value


def prompt_int(message: str) -> int:
    while True:
        raw = input(message).strip()
        try:
            value = int(raw)
        except ValueError:
            print("⚠️  أدخل رقم صحيح / Enter an integer.")
            continue
        return value


def save_receipt(cart: CashierCart, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    receipt_path = output_dir / f"receipt_{timestamp}.csv"

    with receipt_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Qty", "Price", "Total"])
        for item in cart.items.values():
            writer.writerow([item.name, item.quantity, f"{item.price:.2f}", f"{item.total:.2f}"])
        writer.writerow([])
        writer.writerow(["Subtotal", f"{cart.subtotal():.2f}"])
        writer.writerow(["Discount %", f"{cart.discount_percent:.1f}"])
        writer.writerow(["Discount Amount", f"{cart.discount_amount():.2f}"])
        writer.writerow(["Tax %", f"{cart.tax_percent:.1f}"])
        writer.writerow(["Tax Amount", f"{cart.tax_amount():.2f}"])
        writer.writerow(["Total Due", f"{cart.total_due():.2f}"])

    return receipt_path


def run_cashier() -> None:
    cart = CashierCart()
    print_header()

    while True:
        print_menu()
        choice = input("\nاختيارك / Your choice: ").strip()

        if choice == "1":
            print_cart(cart)
        elif choice == "2":
            name = input("اسم الصنف / Item name: ").strip()
            if not name:
                print("⚠️  اسم الصنف مطلوب / Item name is required.")
                continue
            price = prompt_float("سعر الصنف / Item price: ")
            quantity = prompt_int("الكمية / Quantity: ")
            if quantity <= 0:
                print("⚠️  الكمية يجب أن تكون أكبر من صفر / Quantity must be > 0.")
                continue
            cart.add_item(name=name, price=price, quantity=quantity)
            print("✅ تمت الإضافة / Item added.")
        elif choice == "3":
            name = input("اسم الصنف / Item name: ").strip()
            quantity = prompt_int("الكمية الجديدة / New quantity: ")
            if not cart.update_quantity(name, quantity):
                print("⚠️  الصنف غير موجود / Item not found.")
            else:
                print("✅ تم التحديث / Quantity updated.")
        elif choice == "4":
            name = input("اسم الصنف / Item name: ").strip()
            if cart.remove_item(name):
                print("✅ تم الحذف / Item removed.")
            else:
                print("⚠️  الصنف غير موجود / Item not found.")
        elif choice == "5":
            cart.discount_percent = prompt_float("نسبة الخصم % / Discount %: ")
            print("✅ تم تحديث الخصم / Discount updated.")
        elif choice == "6":
            cart.tax_percent = prompt_float("نسبة الضريبة % / Tax %: ")
            print("✅ تم تحديث الضريبة / Tax updated.")
        elif choice == "7":
            if not cart.items:
                print("⚠️  السلة فارغة / Cart is empty.")
                continue
            print_cart(cart)
            output_dir = Path("receipts")
            receipt_path = save_receipt(cart, output_dir)
            print(f"✅ تم حفظ الفاتورة / Receipt saved: {receipt_path}")
            cart.clear()
        elif choice == "8":
            cart.clear()
            print("✅ تم تفريغ السلة / Cart cleared.")
        elif choice == "0":
            print("مع السلامة / Goodbye!")
            break
        else:
            print("⚠️  اختيار غير صالح / Invalid choice.")


if __name__ == "__main__":
    run_cashier()
