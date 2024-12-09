import datetime
import os
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

import mysql.connector
from PIL import Image, ImageTk

image_folder = r"Photos"

# Database Configuration
DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "MySql.Admin"
DB_NAME = "g6cafe"


# Create a connection to the database
def connect_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

#Load menu
menu = {}

def generate_menu():
    connection = connect_db()
    cursor = connection.cursor()

    # generate the list of menu
    cursor.execute("SELECT DISTINCT category_name FROM menu_details")
    categoryRows = cursor.fetchall()

    for categoryRow in categoryRows:
        cat = categoryRow
        catSTR = str(categoryRow[0])
        menu[catSTR] = []

        cursor.execute("SELECT item_id, item_name, unit_price, photo FROM menu_details WHERE category_name = %s", tuple(categoryRow))
        # Fetch all rows
        rows = cursor.fetchall()

        #this is my changes
        # Print the results
        for row in rows:
            item_id, item_name, unit_price, photo = row
            item = {"name": str(item_name), "price": float(unit_price), "image": str(photo), "item_id": item_id}
            if len(menu[catSTR]) == 0:
                menu[catSTR] = [item]
            else:
                menu[catSTR].append(item)

    close_connection(connection)

VAT_RATE = 0.12
DISCOUNT_RATE = 0.20
sales = []  # To track sales data

def close_connection(conn):
    conn.close()

class POSApp:
   def __init__(self, root):
       self.menu = None
       self.tendered_entry = None
       self.discount_details = None
       self.vat_label = None
       self.subtotal_label = None
       self.summary_frame = None
       self.total_label = None
       self.discount_label = None
       self.menu_frame = None
       self.order_listbox = None
       self.create_daily_sales_page = None
       self.root = root
       self.root.title("G6 Cafe")
       self.current_order = {}
       self.is_discount_applied = False
       self.customer_preferences = {}


       # Initialize frames
       generate_menu()
       self.create_home_page()


   def clear_frame(self):
       """Clears the current frame."""
       for widget in self.root.winfo_children():
           widget.destroy()


   def create_home_page(self):
       """Creates the home page."""
       self.clear_frame()
       tk.Label(self.root, text="Welcome to G6 Cafe!", font=("Arial", 25), fg="#8B5E3C").pack(pady=20)
       tk.Button(self.root, text="Take Order", font=("Arial", 15), width=20, height=2, bg="#A98C82", fg="white",
                 command=self.create_order_page).pack(pady=10)
       tk.Button(self.root, text="Sales Report", font=("Arial", 15), width=20, height=2, bg="#A98C82", fg="white",
                 command=self.create_sales_report_page).pack(pady=10)
       tk.Button(self.root, text="Log off", width=10, bg="#765B50", fg="white", command=self.root.destroy).pack(
           side="bottom", pady=50)
       tk.Button(self.root, text="Settings", font=("Arial", 15), width=20, height=2, bg="#A98C82", fg="white",
                 command=self.create_settings_page).pack(pady=10)


   def create_settings_page(self):
       """Displays the Settings page."""
       self.clear_frame()


       tk.Label(self.root, text="Settings", font=("Arial", 18), bg="#F5F5F5").pack(pady=10)


       # Button for adding new products
       tk.Button(self.root, text="Add New Product", font=("Arial", 15), width=20, height=2, bg="#A98C82", fg="white",
                 command=self.add_new_product_page).pack(pady=10)


       # Button for removing products
       tk.Button(self.root, text="Remove Products", font=("Arial", 15), width=20, height=2, bg="#A98C82", fg="white",
                 command=self.remove_products_page).pack(pady=10)


       # Back to Home Page Button
       tk.Button(self.root, text="Back to Home", font=("Arial", 15), width=20, height=2, bg="red", fg="white",
                 command=self.create_home_page).pack(pady=20)


   def add_new_product_page(self):
       """Displays the Add New Product form."""
       self.clear_frame()


       tk.Label(self.root, text="Add New Product", font=("Arial", 18), bg="#F5F5F5").pack(pady=10)


       # Product Name
       tk.Label(self.root, text="Product Name:", font=("Arial", 12), bg="#F5F5F5").pack(anchor="w", padx=20)
       product_name_entry = tk.Entry(self.root, font=("Arial", 12))
       product_name_entry.pack(pady=5)


       # Product Category
       tk.Label(self.root, text="Category:", font=("Arial", 12), bg="#F5F5F5").pack(anchor="w", padx=20)
       category_entry = tk.Entry(self.root, font=("Arial", 12))
       category_entry.pack(pady=5)


       # Product Price
       tk.Label(self.root, text="Price (₱):", font=("Arial", 12), bg="#F5F5F5").pack(anchor="w", padx=20)
       price_entry = tk.Entry(self.root, font=("Arial", 12))
       price_entry.pack(pady=5)


       def add_product():
           name = product_name_entry.get().strip()
           category = category_entry.get().strip()
           try:
               price = float(price_entry.get().strip())
           except ValueError:
               tk.messagebox.showerror("Error", "Invalid price. Please enter a numeric value.")
               return


           if not name or not category:
               tk.messagebox.showerror("Error", "Please fill in all fields.")
               return


           # Add the product to the menu
           if category not in self.menu:  # Check if category exists in the menu
               menu[category] = []  # Create category if it doesn't exist
           menu[category].append({"name": name, "price": price})


           tk.messagebox.showinfo("Success", f"{name} has been added to the {category} category!")


           # Refresh the settings page to show the updated menu
           self.create_settings_page()


       # Add Product Button
       tk.Button(self.root, text="Add Product", font=("Arial", 12), bg="green", fg="white", command=add_product).pack(
           pady=10)


       # Back to Settings Button
       tk.Button(self.root, text="Back to Settings", font=("Arial", 12), bg="red", fg="white",
                 command=self.create_settings_page).pack(pady=10)


   def remove_products_page(self, category_page=1, items_per_category_page=2,
                            items_per_product_page=15):
       """Displays the Remove Products interface with pagination for categories (2 per page) and products."""
       self.clear_frame()


       # Header
       tk.Label(self.root, text="Remove Products", font=("Arial", 18), bg="#F5F5F5").pack(pady=10)


       # Get all categories
       all_categories = list(menu.keys())
       total_categories = len(all_categories)
       total_category_pages = (total_categories + items_per_category_page - 1) // items_per_category_page


       # Get the categories to display on the current page
       start_category_index = (category_page - 1) * items_per_category_page
       end_category_index = start_category_index + items_per_category_page
       categories_to_display = all_categories[start_category_index:end_category_index]


       # Frame for category and product listings
       display_frame = tk.Frame(self.root, bg="#F5F5F5")
       display_frame.pack(fill="both", expand=True, padx=10, pady=10)


       total_height = 0  # Keep track of the height of content


       for category in categories_to_display:
           # Label for category
           category_label = tk.Label(display_frame, text=f"Category: {category}", font=("Arial", 15), bg="#F5F5F5",
                                     fg="blue")
           category_label.pack(anchor="w", padx=20, pady=5)


           total_height += category_label.winfo_height()  # Add category label height to total


           # Products for the current category
           products = menu[category]
           total_product_pages = (len(products) + items_per_product_page - 1) // items_per_product_page


           def display_products(product_page=1):
               nonlocal total_height  # Make sure we update total height as we go


               product_start_index = (product_page - 1) * items_per_product_page
               product_end_index = product_start_index + items_per_product_page
               products_to_display = products[product_start_index:product_end_index]


               # Frame for products
               product_frame = tk.Frame(display_frame, bg="#F5F5F5")
               product_frame.pack(fill="x")


               for product in products_to_display:
                   product_item = tk.Frame(product_frame, bg="#F5F5F5")
                   product_item.pack(anchor="w", padx=40, pady=2, fill="x")


                   # Product label
                   product_label = tk.Label(product_item, text=f"{product['name']} (₱{product['price']:.2f})",
                                            font=("Arial", 12), bg="#F5F5F5")
                   product_label.pack(side="left")


                   # Remove Button
                   def remove_product(p_name=product['name'], p_category=category):
                       menu[p_category] = [p for p in menu[p_category] if p["name"] != p_name]
                       if not menu[p_category]:  # Remove empty category
                           del menu[p_category]
                       tk.messagebox.showinfo("Success", f"{p_name} has been removed.")
                       self.remove_products_page(category_page)  # Refresh the page


                   remove_button = tk.Button(product_item, text="Remove", font=("Arial", 10), bg="red", fg="white",
                                             command=remove_product)
                   remove_button.pack(side="right")


                   total_height += product_item.winfo_height()  # Add product item height to total


               # Product navigation buttons
               nav_frame = tk.Frame(product_frame, bg="#F5F5F5")
               nav_frame.pack(pady=5)


               if product_page > 1:
                   prev_button = tk.Button(nav_frame, text="Previous Products", font=("Arial", 10), bg="blue",
                                           fg="white", command=lambda: display_products(product_page - 1))
                   prev_button.pack(side="left", padx=5)


               if product_page < total_product_pages:
                   next_button = tk.Button(nav_frame, text="Next Products", font=("Arial", 10), bg="blue", fg="white",
                                           command=lambda: display_products(product_page + 1))
                   next_button.pack(side="left", padx=5)


               total_height += nav_frame.winfo_height()  # Add nav height to total


           display_products()


       # Check if the total content exceeds the available screen space
       screen_height = 768  # Standard screen height for 1024x768 resolution
       if total_height > screen_height:
           # Add "Next Page" button if content exceeds the available screen space
           nav_frame = tk.Frame(self.root, bg="#F5F5F5")
           nav_frame.pack(pady=10)


           if category_page < total_category_pages:
               next_categories_button = tk.Button(nav_frame, text="Next Categories", font=("Arial", 12), bg="green",
                                                  fg="white",
                                                  command=lambda: self.remove_products_page(category_page + 1))
               next_categories_button.pack(side="left", padx=10)


       # Category navigation
       nav_frame = tk.Frame(self.root, bg="#F5F5F5")
       nav_frame.pack(pady=10)


       if category_page > 1:
           prev_categories_button = tk.Button(nav_frame, text="Previous Categories", font=("Arial", 12), bg="green",
                                              fg="white", command=lambda: self.remove_products_page(category_page - 1))
           prev_categories_button.pack(side="left", padx=10)


       if category_page < total_category_pages:
           next_categories_button = tk.Button(nav_frame, text="Next Categories", font=("Arial", 12), bg="green",
                                              fg="white", command=lambda: self.remove_products_page(category_page + 1))
           next_categories_button.pack(side="left", padx=10)


       # Back to Settings Button
       tk.Button(self.root, text="Back to Settings", font=("Arial", 12), bg="red", fg="white",
                 command=self.create_settings_page).pack(pady=10)


   def create_order_page(self):
       """Creates the order page."""
       self.clear_frame()


       # Category Frame
       category_frame = tk.Frame(self.root, width=200, bg="#D3D3D3")
       category_frame.pack(side="left", fill="y")
       tk.Label(category_frame, text="Menu Category", font=("Arial", 20), bg="#D3D3D3").pack(pady=10, padx=15)


       for category in menu.keys():
           tk.Button(category_frame, text=category, font=("Arial", 15), width=15, height=2,
                     command=lambda c=category: self.show_menu_items(c)).pack(pady=5)


       tk.Button(category_frame, text="Back", width=20, bg="red", fg="white", command=self.create_home_page).pack(
           side="bottom", pady=10)

       connection = connect_db()
       cursor = connection.cursor()
       cursor.execute("SELECT DISTINCT category_name FROM menu_details LIMIT 1")
       cat = cursor.fetchone()

       # Menu Items Frame
       self.menu_frame = tk.Frame(self.root, bg="#F5F5F5")
       self.menu_frame.pack(side="left", fill="both", expand=True)
       self.show_menu_items(str(cat[0])) #get initial category


       # Order Summary Frame (centered)
       self.summary_frame = tk.Frame(self.root, bg="#EFEFEF", padx=10, pady=10, relief="solid")
       self.summary_frame.pack(side="right", fill="y", padx=20)
       tk.Label(self.summary_frame, text="Order Summary", font=("Arial", 16), bg="#EFEFEF").pack(pady=10)


       self.order_listbox = tk.Listbox(self.summary_frame, width=40, height=15)
       self.order_listbox.pack(pady=5)


       self.subtotal_label = tk.Label(self.summary_frame, text="Subtotal: ₱0.00", font=("Arial", 12), bg="#EFEFEF",
                                      anchor="w")
       self.subtotal_label.pack(fill="x", padx=10)
       self.vat_label = tk.Label(self.summary_frame, text="VAT (12%): ₱0.00", font=("Arial", 12), bg="#EFEFEF",
                                 anchor="w")
       self.vat_label.pack(fill="x", padx=10)
       self.discount_label = tk.Label(self.summary_frame, text="Discount: ₱0.00", font=("Arial", 12), bg="#EFEFEF",
                                      anchor="w")
       self.discount_label.pack(fill="x", padx=10)
       self.total_label = tk.Label(self.summary_frame, text="Total: ₱0.00", font=("Arial", 12, "bold"), bg="#EFEFEF",
                                   anchor="w")
       self.total_label.pack(fill="x", padx=10)


       tk.Button(self.summary_frame, text="Set Preferences", bg="#FF6347", fg="white",
                 command=self.set_preferences_for_selected_item).pack(pady=5)
       tk.Button(self.summary_frame, text="Remove Selected Item", bg="#FF6347", fg="white",
                 command=self.remove_selected_item).pack(pady=5)
       tk.Button(self.summary_frame, text="PWD/Senior Citizen Discount", bg="#FF6347", fg="white",
                 command=self.apply_discount).pack(pady=5)
       tk.Label(self.summary_frame, text="Amount Tendered:", bg="#EFEFEF").pack(pady=5)
       self.tendered_entry = tk.Entry(self.summary_frame)
       self.tendered_entry.pack(pady=5)
       tk.Button(self.summary_frame, text="Proceed Payment", bg="green", fg="white", command=self.checkout).pack(
           pady=20)


   def set_preferences_for_selected_item(self):
       """Sets preferences for the selected item with a custom dialog box."""
       selected = self.order_listbox.curselection()
       if not selected:
           messagebox.showerror("Error", "No item selected!")
           return


       # Extract item name from the selected line
       item_name = self.order_listbox.get(selected).split(" x")[0]


       # Create custom dialog for setting preferences
       dialog = tk.Toplevel(self.root)
       dialog.title("Customer Preferences")
       dialog.geometry("400x250")  # Set custom size (width x height)
       dialog.transient(self.root)  # Make it a child of the main window
       dialog.grab_set()  # Make it modal


       tk.Label(dialog, text=f"Enter preferences for {item_name}:", font=("Arial", 14)).pack(pady=10)
       preferences_entry = tk.Text(dialog, height=5, width=40, wrap="word")
       preferences_entry.pack(pady=10)


       def save_preferences():
           preferences = preferences_entry.get("1.0", tk.END).strip()
           if preferences:
               self.customer_preferences[item_name] = preferences
               self.update_order_summary()
           dialog.destroy()


       tk.Button(dialog, text="Save", bg="green", fg="white", command=save_preferences).pack(pady=10)
       tk.Button(dialog, text="Cancel", bg="red", fg="white", command=dialog.destroy).pack()


   # noinspection PyTypeChecker
   def show_menu_items(self, category):
       """Displays menu items of a selected category."""
       for widget in self.menu_frame.winfo_children():
           widget.destroy()


       tk.Label(self.menu_frame, text=f"{category} Menu", font=("Arial", 14), bg="#F5F5F5").pack(pady=10)


       for item in menu[category]:
           frame = tk.Frame(self.menu_frame, bg="#F5F5F5", pady=10)
           frame.pack(fill="x", padx=20)


           image_path = os.path.join(image_folder, item["image"])  # Combine folder and image filename
           #image_path = "C:/Users/Friend/Downloads/image/americano.jpg"
           try:
               image = Image.open(image_path).resize((80, 80))  # Resize image
               photo = ImageTk.PhotoImage(image)  # Create PhotoImage instance
               img_label = tk.Label(frame, image=photo, bg="#F5F5F5")  # Use 'image=photo'
               img_label.image = photo  # Keep a reference to prevent garbage collection
               img_label.pack(side="left", padx=10)
           except FileNotFoundError:
               tk.Label(frame, text="No Image", width=10, height=5, bg="#D3D3D3").pack(side="left", padx=10)


           # Details and Add Button
           details_frame = tk.Frame(frame, bg="#F5F5F5")
           details_frame.pack(side="left", fill="x")
           tk.Label(details_frame, text=item["name"], font=("Arial", 12), bg="#F5F5F5").pack(anchor="w")
           tk.Label(details_frame, text=f"₱{item['price']:.2f}", font=("Arial", 12), bg="#F5F5F5").pack(anchor="w")


           # Quantity Spinbox and Add Button
           quantity_spinbox = tk.Spinbox(frame, from_=1, to=100, width=5)
           quantity_spinbox.pack(side="right", padx=5)
           tk.Button(frame, text="Add", bg="#D2B48C", fg="white",
                     command=lambda i=item, q=quantity_spinbox: self.add_to_order(i, int(q.get()))).pack(side="right",
                                                                                                         padx=5)


   def add_to_order(self, item, quantity):
       """Adds an item with a specific quantity to the current order."""
       if quantity <= 0:
           messagebox.showerror("Error", "Quantity must be greater than zero.")
           return


       self.current_order[item["name"]] = self.current_order.get(item["name"], 0) + quantity
       self.update_order_summary()


   def remove_selected_item(self):
       """Removes the selected item from the order."""
       selected = self.order_listbox.curselection()
       if not selected:
           messagebox.showerror("Error", "No item selected!")
           return


       item_name = self.order_listbox.get(selected).split(" x")[0]  # Extract the item name
       if item_name in self.current_order:
           del self.current_order[item_name]
           self.update_order_summary()


   def update_order_summary(self):
       """Updates the order summary."""
       self.order_listbox.delete(0, tk.END)
       subtotal = 0


       # Calculate the subtotal for all items in the current order
       for item, qty in self.current_order.items():
           # Fetch price from menu
           price = next(i["price"] for cat in menu.values() for i in cat if i["name"] == item)


           # Display item and quantity
           self.order_listbox.insert(tk.END, f"{item} x{qty} = ₱{price * qty:.2f}")
           subtotal += price * qty


           # Check and display customer preferences if available
           if item in self.customer_preferences:
               preference_text = f"    - Preferences: {self.customer_preferences[item]}"
               self.order_listbox.insert(tk.END, preference_text)


       # Apply VAT and discount logic
       if self.is_discount_applied:
           # Remove VAT if the discount is applied
           discount = subtotal * DISCOUNT_RATE
           vat = 0  # VAT is not applied with discount
           total = subtotal - discount
       else:
           # Calculate VAT normally if no discount is applied
           vat = subtotal * VAT_RATE
           discount = 0
           total = subtotal + vat


       # Update UI elements for order summary
       self.subtotal_label.config(text=f"Amount Due: ₱{subtotal:.2f}")
       self.vat_label.config(text=f"VAT (12%): ₱{vat:.2f}")
       self.discount_label.config(text=f"Discount: ₱{discount:.2f}")
       self.total_label.config(text=f"Total: ₱{total:.2f}")


   def apply_discount(self):
       """Applies or removes the discount based on the current state."""
       if not self.current_order:
           messagebox.showerror("Error", "No items in the order to apply a discount!")
           return


       if self.is_discount_applied:
           # Remove the discount
           self.is_discount_applied = False
           self.discount_details = None  # Clear previous discount details
           messagebox.showinfo("Discount Removed", "Discount has been removed, VAT reapplied.")
       else:
           # Show popup to collect Name, ID Number, and Discount Type
           def confirm_discount():
               name = name_entry.get().strip()
               id_number = id_entry.get().strip()
               discount_type = discount_type_var.get()


               if not name or not id_number or discount_type == "Select Type":
                   messagebox.showerror("Error", "All fields (Name, ID Number, and Type) are required!")
                   return


               # Apply the discount
               self.is_discount_applied = True
               self.discount_details = {
                   "name": name,
                   "id_number": id_number,
                   "type": discount_type
               }
               discount_window.destroy()
               messagebox.showinfo("Discount Applied",
                                   f"20% discount applied for {discount_type} ({name})! VAT has been removed.")


               # Update the order summary to reflect the changes
               self.update_order_summary()


           # Create a popup window for PWD/Senior Citizen details
           discount_window = tk.Toplevel(self.root)
           discount_window.title("Discount Details")
           discount_window.geometry("400x350")
           discount_window.resizable(False, False)
           discount_window.grab_set()  # Ensure focus remains on this window


           tk.Label(discount_window, text="Enter Discount Details", font=("Arial", 12)).pack(pady=10)


           tk.Label(discount_window, text="Name:", font=("Arial", 10)).pack(anchor="w", padx=10)
           name_entry = tk.Entry(discount_window, width=30)
           name_entry.pack(padx=10, pady=5)


           tk.Label(discount_window, text="ID Number:", font=("Arial", 10)).pack(anchor="w", padx=10)
           id_entry = tk.Entry(discount_window, width=30)
           id_entry.pack(padx=10, pady=5)


           tk.Label(discount_window, text="Discount Type:", font=("Arial", 10)).pack(anchor="w", padx=10)
           discount_type_var = tk.StringVar(value="Select Type")
           discount_type_menu = tk.OptionMenu(discount_window, discount_type_var, "PWD", "Senior Citizen")
           discount_type_menu.pack(padx=10, pady=5)


           tk.Button(discount_window, text="Confirm", command=confirm_discount, bg="#4CAF50", fg="white").pack(pady=10)


       # Update the order summary after toggling the discount
       self.update_order_summary()


   def checkout(self):
       """Finalizes the order."""
       if not self.current_order:
           messagebox.showerror("Error", "No items in the order!")
           return


       # Validate tendered amount
       try:
           tendered = float(self.tendered_entry.get())
       except ValueError:
           messagebox.showerror("Error", "Invalid tendered amount!")
           return


       # Calculate the total amount dynamically
       subtotal = sum(
           next(i["price"] for cat in menu.values() for i in cat if i["name"] == item) * qty
           for item, qty in self.current_order.items()
       )


       if self.is_discount_applied:
           discount = subtotal * DISCOUNT_RATE
           var = 0
           total = subtotal - discount
       else:
           vat = subtotal * VAT_RATE
           discount = 0
           total = subtotal + vat


       # Check if the tendered amount is sufficient
       if tendered < total:
           messagebox.showerror("Error", "Amount tendered is less than total amount!")
           return


       # Generate receipt number and current date/time
       receipt_number = f"REC{datetime.datetime.now().strftime("%Y%m%d%H%M")}"
       current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


       # Generate receipt text
       receipt_lines = [
           "========================================",
           "              G6 Cafe                ",
           f"        Receipt #: {receipt_number}    ",
           f"          Date: {current_datetime}    ",
           "=========================================",
           f"{'Item':<20}{'Qty':^8}{'Subtotal':>12}",
           "------------------------------------------"
       ]


       subtotal = 0
       for item, qty in self.current_order.items():
           price = next(i["price"] for cat in menu.values() for i in cat if i["name"] == item)
           item_total = price * qty
           receipt_lines.append(f"{item:<20}{qty:^8}₱{item_total:>10.2f}")
           subtotal += item_total


           # Add preferences if they exist
           if item in self.customer_preferences:
               preferences = self.customer_preferences[item]
               receipt_lines.append(f"   - Preferences: {preferences}")


       # Apply discount and VAT logic
       if self.is_discount_applied:
           discount = subtotal * 0.20  # 20% discount
           vat = 0  # No VAT if discount is applied
       else:
           discount = 0
           vat = subtotal * VAT_RATE  # Normal 12% VAT


       total = subtotal + vat - discount
       change = max(0, tendered - total)  # Ensure no negative change


       # Add financial summary
       receipt_lines.extend([
           "------------------------------------------",
           f"{'Amount Due:':<30}₱{subtotal:>10.2f}",
           f"{'VAT (12%):':<30}₱{vat:>10.2f}",
           f"{'Discount (20%):':<30}-₱{discount:>9.2f}",
           "===========================================",
           f"{'Total:':<30}₱{total:>10.2f}",
           f"{'Amount Tendered:':<30}₱{tendered:>10.2f}",
           f"{'Change:':<30}₱{change:>10.2f}",
       ])



       # Add discount details if applicable
       disc_name = ""
       disc_id_number = ""
       disc_type = ""
       if self.is_discount_applied and self.discount_details:
           receipt_lines.extend([
               "--------------------------------------",
               "Discount Details:",
               f"  Type: {self.discount_details['type']}",
               f"  Name: {self.discount_details['name']}",
               f"  ID Number: {self.discount_details['id_number']}",
           ])

           disc_name = self.discount_details['name']
           disc_id_number = self.discount_details['id_number']
           disc_type = self.discount_details['type']


       # Closing receipt lines
       receipt_lines.extend([
           "======================================",
           "   Thank You for choosing our Coffee  ",
           "      Have a Great Day! Come Again!   ",
           "======================================"
       ])


       # Display or save the receipt (not shown here)


       receipt_text = "\n".join(receipt_lines)

       #Insert to orders table
       conn = connect_db()
       cur = conn.cursor()

       insert_order = (f"INSERT INTO orders (subtotal, vat_amount, discount_amount, net_amount, "
                       f"tender_amount, change_amount, receipt_number)"
                       f" VALUES (%s, %s, %s, %s, %s, %s, %s)")

       cur.execute(insert_order, (subtotal, vat, discount, total, tendered, change, receipt_number))
       order_id = cur.lastrowid

       insert_order_details = ("INSERT INTO order_details (order_id, item_id, quantity, subtotal, order_preference)"
                               "VALUES (%s, %s, %s, %s, %s)")

       item_subtotal = 0
       for ord_item, qty in self.current_order.items():
           price = next(i["price"] for item_cat in menu.values() for i in item_cat if i["name"] == ord_item)
           item_id = next(i["item_id"] for item_cat in menu.values() for i in item_cat if i["name"] == ord_item)
           item_total = price * qty
           item_subtotal += item_total

           # Add preferences if they exist
           if ord_item in self.customer_preferences:
               preferences = self.customer_preferences[ord_item]
               cur.execute(insert_order_details, (order_id, item_id, qty, item_subtotal, preferences))
           else:
               cur.execute(insert_order_details, (order_id, item_id, qty, item_subtotal, ""))



       if self.is_discount_applied:
           insert_pwd = ("INSERT INTO pwdsenior_details (order_id, discount_type, customer_name, id_number, discount_amount)"
                         "VALUES (%s, %s, %s, %s, %s)")
           cur.execute(insert_pwd, (order_id, disc_type, disc_name, disc_id_number, discount))

       conn.commit()
       close_connection(conn)

       # Display receipt in a new window
       receipt_window = tk.Toplevel(self.root)
       receipt_window.title("Receipt")
       receipt_window.geometry("500x600")


       receipt_label = tk.Label(receipt_window, text=receipt_text, font=("Courier", 12), justify="left")
       receipt_label.pack(padx=20, pady=20)


       # Add 'OK' button to close the receipt window
       def close_receipt():
           receipt_window.destroy()


       # Add 'Back to Main Menu' button
       def go_back_to_main_menu():
           receipt_window.destroy()
           self.create_home_page()


       ok_button = tk.Button(receipt_window, text="OK", command=close_receipt, bg="green", fg="white")
       ok_button.pack(side="left", padx=20, pady=10)


       back_button = tk.Button(receipt_window, text="Back to Main Menu", command=go_back_to_main_menu, bg="orange",
                               fg="white")
       back_button.pack(side="right", padx=20, pady=10)


       # Reset the order
       self.current_order.clear()
       self.is_discount_applied = False
       self.update_order_summary()
       self.tendered_entry.delete(0, tk.END)


   def create_sales_report_page(self):
       """Displays the sales report."""
       self.clear_frame()


       # Sidebar navigation
       sidebar = tk.Frame(self.root, bg="#4A4A4A", width=200)
       sidebar.pack(side="left", fill="y")


       tk.Button(sidebar, text="Daily Sale \nSummary", font=("Arial", 12), bg="#A98C82", fg="white", width=15,
                 height=2,
                 command=self.create_sales_report_page).pack(pady=10, padx=10)
       tk.Button(sidebar, text="Sales Invoice", font=("Arial", 12), bg="#A98C82", fg="white", width=15, height=2,
                 command=self.create_daily_sales_page).pack(pady=10)


       # Main report frame
       report_frame = tk.Frame(self.root, bg="#D3D3D3", padx=10, pady=10)
       report_frame.pack(side="right", fill="both", expand=True)


       # Header with current date
       tk.Label(report_frame, text=datetime.datetime.now().strftime("%A, %B %d, %Y"),
                font=("Arial", 14), bg="#D3D3D3").pack(anchor="ne", pady=10, padx=10)


       # Sale Summary section
       summary_frame = tk.Frame(report_frame, bg="#D3D3D3")
       summary_frame.pack(fill="x", pady=10)


       # Calculate sales totals
       sales_conn = connect_db()
       sales_cur = sales_conn.cursor()
       sales_cur.execute("SELECT * FROM vwmonthlysales")
       m_sum = sales_cur.fetchone()

       monthly_sales = float(m_sum[0])

       sales_cur.execute("SELECT * FROM vwyearlysales")
       y_sum = sales_cur.fetchone()

       yearly_sales = float(y_sum[0])


       # Summary Cards
       tk.Label(summary_frame, text="SALES REPORT", font=("Arial", 16, "bold"), bg="#D3D3D3").pack(pady=10)


       card_frame = tk.Frame(summary_frame, bg="#D3D3D3")
       card_frame.pack()


       monthly_card = tk.Frame(card_frame, bg="#4A4A4A", padx=20, pady=10)
       monthly_card.grid(row=0, column=0, padx=20, pady=10)
       tk.Label(monthly_card, text="Monthly Sales", font=("Arial", 12), bg="#4A4A4A", fg="white").pack()
       tk.Label(monthly_card, text=f"₱{monthly_sales:,.2f}", font=("Arial", 20, "bold"), bg="#4A4A4A",
                fg="white").pack()


       yearly_card = tk.Frame(card_frame, bg="#4A4A4A", padx=20, pady=10)
       yearly_card.grid(row=0, column=1, padx=20, pady=10)
       tk.Label(yearly_card, text="Yearly Sales", font=("Arial", 12), bg="#4A4A4A", fg="white").pack()
       tk.Label(yearly_card, text=f"₱{yearly_sales:,.2f}", font=("Arial", 20, "bold"), bg="#4A4A4A", fg="white").pack()


       # Daily Sale Summary Table
       tk.Label(report_frame, text="DAILY SALE SUMMARY", font=("Arial", 14), bg="#D3D3D3").pack(pady=10)


       columns = ("date", "item", "qty", "discount", "amount")
       tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=10)
       tree.heading("date", text="Date")
       tree.heading("item", text="Item")
       tree.heading("qty", text="Quantity")
       tree.heading("discount", text="Discount Amount")
       tree.heading("amount", text="Amount")


       # Format column widths
       tree.column("date", width=120, anchor="center")
       tree.column("item", width=200, anchor="w")
       tree.column("qty", width=80, anchor="center")
       tree.column("discount", width=120, anchor="e")
       tree.column("amount", width=120, anchor="e")


       # Invoice Table
       columns = ("date", "receipt", "item", "qty", "amount")
       tree = ttk.Treeview(report_frame, columns=columns, show="headings", height=15)
       tree.heading("date", text="Date")
       tree.heading("receipt", text="Receipt #")
       tree.heading("item", text="Item")
       tree.heading("qty", text="Quantity")
       tree.heading("amount", text="Amount")

       sales_cur.execute("SELECT date_time, receipt_number, item_name, quantity, subtotal FROM vwdaily_sales_report")
       sales_daily = sales_cur.fetchall()

       # Populate the table with sales data
       # for sale in sales:
       for date_time, receipt_number, item_name, quantity, subtotal in sales_daily:
           tree.insert("", "end", values=(
               date_time,
               receipt_number,
               item_name,
               quantity,
               f"₱{subtotal:,.2f}"
           ))

           # for item_name, details in sale["order"].items():
           #     quantity = details["quantity"]
           #     price = details["price"]
           #     item_total = price * quantity
           #     discount_amount = sale.get("discount", 0)  # Retrieve discount amount if available
           #     tree.insert(
           #         "",
           #         "end",
           #         values=(
           #             sale_date,
           #             item_name,
           #             quantity,
           #             f"₱{discount_amount:.2f}",
           #             f"₱{item_total:.2f}"
           #         ),
           #     )


       tree.pack(fill="both", expand=True, pady=10)


       # Back Button
       tk.Button(report_frame, text="Back to Home", bg="red", fg="white", command=self.create_home_page).pack(pady=10)




if __name__ == "__main__":
   root = tk.Tk()
   root.geometry("1024x960")
   app = POSApp(root)
   root.mainloop()