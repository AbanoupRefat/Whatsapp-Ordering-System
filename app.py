import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import urllib.parse
import math

# Page Configuration
st.set_page_config(
    page_title="شركة المهندس لقطع غيار السيارات",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Arabic RTL and Mobile-First Design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@200;300;400;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    /* Header Styles */
    .company-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .company-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .company-subtitle {
        font-size: 1.1rem;
        font-weight: 300;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Mobile-First Table Container */
    .mobile-table-container {
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scroll-snap-type: x proximity;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1rem 0;
        background: white;
    }
    
    .products-table {
        min-width: 700px;
        width: 100%;
        border-collapse: collapse;
        font-family: 'Cairo', sans-serif;
    }
    
    .table-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        position: sticky;
        top: 0;
        z-index: 100;
    }
    
    .table-header th {
        padding: 1rem 0.5rem;
        font-weight: 600;
        text-align: center;
        border-right: 1px solid rgba(255,255,255,0.2);
    }
    
    .table-row {
        border-bottom: 1px solid #e2e8f0;
        transition: background-color 0.2s;
    }
    
    .table-row:hover {
        background-color: #f8fafc;
    }
    
    .table-cell {
        padding: 0.75rem 0.5rem;
        text-align: center;
        border-right: 1px solid #e2e8f0;
    }
    
    .product-name {
        max-width: 200px;
        word-wrap: break-word;
        text-align: right;
        font-weight: 500;
    }
    
    .price-cell {
        font-weight: 600;
        color: #059669;
    }
    
    .quantity-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .quantity-btn {
        background: #667eea;
        color: white;
        border: none;
        border-radius: 6px;
        width: 30px;
        height: 30px;
        cursor: pointer;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .quantity-btn:hover {
        background: #5a67d8;
        transform: scale(1.1);
    }
    
    .quantity-display {
        background: #f7fafc;
        border: 2px solid #e2e8f0;
        border-radius: 6px;
        width: 40px;
        height: 30px;
        text-align: center;
        font-weight: 600;
        line-height: 26px;
    }
    
    .subtotal-cell {
        background: #f0f9f4;
        font-weight: 700;
        color: #059669;
    }
    
    /* Category Separator */
    .category-separator {
        background: linear-gradient(90deg, #f7fafc 0%, #e2e8f0 50%, #f7fafc 100%);
        height: 3px;
    }
    
    /* Search and Filter Controls */
    .search-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Cart Summary */
    .cart-summary {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        text-align: center;
    }
    
    .cart-stats {
        display: flex;
        justify-content: space-around;
        margin-top: 1rem;
    }
    
    .cart-stat {
        text-align: center;
    }
    
    .cart-stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        display: block;
    }
    
    .cart-stat-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.25rem;
    }
    
    /* Pagination */
    .pagination-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    
    .pagination-btn {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Cairo', sans-serif;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    .pagination-btn:hover:not(:disabled) {
        background: #5a67d8;
        transform: translateY(-1px);
    }
    
    .pagination-btn:disabled {
        background: #cbd5e0;
        cursor: not-allowed;
    }
    
    /* WhatsApp Button */
    .whatsapp-btn {
        background: linear-gradient(135deg, #25d366 0%, #128c7e 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-top: 1rem;
        font-family: 'Cairo', sans-serif;
        transition: all 0.3s;
    }
    
    .whatsapp-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(37, 211, 102, 0.3);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .company-title {
            font-size: 1.5rem;
        }
        
        .products-table {
            min-width: 600px;
        }
        
        .table-header th,
        .table-cell {
            padding: 0.5rem 0.25rem;
            font-size: 0.9rem;
        }
        
        .cart-stats {
            flex-direction: column;
            gap: 1rem;
        }
        
        .pagination-container {
            gap: 0.5rem;
        }
        
        .pagination-btn {
            padding: 0.4rem 0.8rem;
            font-size: 0.9rem;
        }
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stDeployButton {display: none;}
    .stDecoration {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = 1
if 'show_order_form' not in st.session_state:
    st.session_state.show_order_form = False
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
if 'origin_filter' not in st.session_state:
    st.session_state.origin_filter = "الكل"

# Cache function for loading Google Sheets data
@st.cache_data
def load_google_sheet():
    """Load data from Google Sheets using service account credentials"""
    try:
        # Get credentials from Streamlit secrets
        credentials_dict = dict(st.secrets["gcp_service_account"])
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets.readonly',
            'https://www.googleapis.com/auth/drive.readonly'
        ]
        
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
        gc = gspread.authorize(credentials)
        
        # Open the Google Sheet
        sheet_id = st.secrets["google"]["sheet_id"]
        sheet = gc.open_by_key(sheet_id).sheet1
        
        # Get all values
        data = sheet.get_all_values()
        
        if not data:
            return pd.DataFrame()
        
        # Convert to DataFrame
        df = pd.DataFrame(data[1:], columns=data[0])  # First row as headers
        
        # Process data - handle empty rows as category separators
        processed_data = []
        current_category = ""
        
        for _, row in df.iterrows():
            if pd.isna(row.iloc[1]) or row.iloc[1] == "":  # Empty البند column
                current_category = row.iloc[0] if not pd.isna(row.iloc[0]) else ""
            else:
                processed_data.append({
                    'الفئة': current_category,
                    'البند': row.iloc[1],
                    'المنشأ': row.iloc[2] if len(row) > 2 else "",
                    'السعر': row.iloc[3] if len(row) > 3 else "0"
                })
        
        return pd.DataFrame(processed_data)
        
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {str(e)}")
        return pd.DataFrame()

def update_quantity(product_name, price, change):
    """Update product quantity in cart"""
    if product_name not in st.session_state.cart:
        st.session_state.cart[product_name] = {'quantity': 0, 'price': price}
    
    new_quantity = st.session_state.cart[product_name]['quantity'] + change
    
    if new_quantity <= 0:
        if product_name in st.session_state.cart:
            del st.session_state.cart[product_name]
    else:
        st.session_state.cart[product_name]['quantity'] = new_quantity

def generate_whatsapp_message():
    """Generate WhatsApp message with order details"""
    if not st.session_state.cart:
        return ""
    
    message_lines = [
        "🌟 *شركة المهندس لقطع غيار السيارات* 🌟",
        "",
        f"📅 *تاريخ الطلب:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "📋 *تفاصيل الطلبية:*",
        ""
    ]
    
    total_cost = 0
    total_items = 0
    
    for product, details in st.session_state.cart.items():
        quantity = details['quantity']
        price = float(details['price'])
        subtotal = quantity * price
        total_cost += subtotal
        total_items += quantity
        
        message_lines.append(f"🔹 *{product}*")
        message_lines.append(f"   الكمية: {quantity}")
        message_lines.append(f"   السعر: {price} ج.م")
        message_lines.append(f"   الإجمالي: {subtotal} ج.م")
        message_lines.append("")
    
    message_lines.extend([
        "─" * 30,
        "📊 *ملخص الطلبية:*",
        f"   📦 عدد الأصناف: {len(st.session_state.cart)}",
        f"   🛒 إجمالي القطع: {total_items}",
        f"   💰 الإجمالي النهائي: *{total_cost:.2f} ج.م*",
        "",
        "شكراً لثقتكم بنا! 🙏",
        "سيتم التواصل معكم قريباً لتأكيد الطلبية."
    ])
    
    return "\n".join(message_lines)

def main():
    # Company Header
    st.markdown("""
    <div class="company-header">
        <h1 class="company-title">🚗 شركة المهندس لقطع غيار السيارات</h1>
        <p class="company-subtitle">متخصصون في توفير قطع غيار السيارات الأصلية والبديلة</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    df = load_google_sheet()
    
    if df.empty:
        st.warning("⚠️ لا توجد بيانات متاحة حالياً. يرجى المحاولة لاحقاً.")
        return
    
    # Sidebar for cart summary
    with st.sidebar:
        st.markdown("### 🛒 سلة التسوق")
        
        if st.session_state.cart:
            total_cost = sum(details['quantity'] * float(details['price']) 
                           for details in st.session_state.cart.values())
            total_items = sum(details['quantity'] for details in st.session_state.cart.values())
            
            st.markdown(f"""
            <div class="cart-summary">
                <div class="cart-stats">
                    <div class="cart-stat">
                        <span class="cart-stat-number">{len(st.session_state.cart)}</span>
                        <span class="cart-stat-label">أصناف</span>
                    </div>
                    <div class="cart-stat">
                        <span class="cart-stat-number">{total_items}</span>
                        <span class="cart-stat-label">قطعة</span>
                    </div>
                    <div class="cart-stat">
                        <span class="cart-stat-number">{total_cost:.0f} ج.م</span>
                        <span class="cart-stat-label">الإجمالي</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📱 إرسال الطلبية عبر واتساب", key="whatsapp_sidebar"):
                message = generate_whatsapp_message()
                whatsapp_number = st.secrets["whatsapp"]["number"]
                whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(message)}"
                st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">📱 فتح واتساب</a>', 
                           unsafe_allow_html=True)
        else:
            st.info("السلة فارغة")
    
    # Search and Filter Section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_query = st.text_input("🔍 البحث في المنتجات", 
                                   value=st.session_state.search_query,
                                   placeholder="ابحث عن قطع الغيار...")
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.session_state.current_page = 1
    
    with col2:
        origins = ["الكل"] + sorted(df['المنشأ'].unique().tolist())
        origin_filter = st.selectbox("تصفية حسب المنشأ", origins, 
                                   index=origins.index(st.session_state.origin_filter))
        if origin_filter != st.session_state.origin_filter:
            st.session_state.origin_filter = origin_filter
            st.session_state.current_page = 1
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data
    filtered_df = df.copy()
    
    if st.session_state.search_query:
        filtered_df = filtered_df[filtered_df['البند'].str.contains(
            st.session_state.search_query, case=False, na=False)]
    
    if st.session_state.origin_filter != "الكل":
        filtered_df = filtered_df[filtered_df['المنشأ'] == st.session_state.origin_filter]
    
    # Pagination
    items_per_page = 15
    total_items = len(filtered_df)
    total_pages = math.ceil(total_items / items_per_page) if total_items > 0 else 1
    
    # Ensure current page is valid
    if st.session_state.current_page > total_pages:
        st.session_state.current_page = 1
    
    start_idx = (st.session_state.current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = filtered_df.iloc[start_idx:end_idx]
    
    # Results info
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0; font-size: 1.1rem; font-weight: 500;">
        📊 عرض {len(page_df)} من أصل {total_items} منتج | صفحة {st.session_state.current_page} من {total_pages}
    </div>
    """, unsafe_allow_html=True)
    
    # Products Table
    if not page_df.empty:
        st.markdown('<div class="mobile-table-container">', unsafe_allow_html=True)
        
        table_html = """
        <table class="products-table">
            <thead class="table-header">
                <tr>
                    <th style="width: 250px;">البند</th>
                    <th style="width: 100px;">المنشأ</th>
                    <th style="width: 80px;">السعر</th>
                    <th style="width: 120px;">الكمية</th>
                    <th style="width: 100px;">الإجمالي</th>
                </tr>
            </thead>
            <tbody>
        """
        
        current_category = ""
        for _, row in page_df.iterrows():
            # Category separator
            if row['الفئة'] != current_category and row['الفئة']:
                current_category = row['الفئة']
                table_html += f"""
                <tr class="category-separator">
                    <td colspan="5" style="text-align: center; font-weight: 600; padding: 0.5rem; background: #f7fafc; color: #4a5568;">
                        {current_category}
                    </td>
                </tr>
                """
            
            product_name = row['البند']
            origin = row['المنשأ'] if 'المنشأ' in row else row.get('المنشأ', '')
            price = float(row['السعر']) if row['السعر'] else 0
            
            # Get current quantity from cart
            current_qty = st.session_state.cart.get(product_name, {}).get('quantity', 0)
            subtotal = current_qty * price
            
            table_html += f"""
            <tr class="table-row">
                <td class="table-cell product-name">{product_name}</td>
                <td class="table-cell">{origin}</td>
                <td class="table-cell price-cell">{price:.0f} ج.م</td>
                <td class="table-cell">
                    <div class="quantity-controls">
                        <button class="quantity-btn" onclick="updateQuantity('{product_name}', {price}, -1)">➖</button>
                        <div class="quantity-display">{current_qty}</div>
                        <button class="quantity-btn" onclick="updateQuantity('{product_name}', {price}, 1)">➕</button>
                    </div>
                </td>
                <td class="table-cell subtotal-cell">{subtotal:.0f} ج.م</td>
            </tr>
            """
        
        table_html += """
            </tbody>
        </table>
        """
        
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # JavaScript for quantity updates
        st.markdown("""
        <script>
        function updateQuantity(productName, price, change) {
            // This will be handled by Streamlit buttons instead
            console.log('Quantity update requested:', productName, price, change);
        }
        </script>
        """, unsafe_allow_html=True)
        
        # Quantity control buttons (hidden, but functional)
        for _, row in page_df.iterrows():
            product_name = row['البند']
            price = float(row['السعر']) if row['السعر'] else 0
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"➕ {product_name}", key=f"add_{product_name}", 
                           help="إضافة قطعة", type="secondary"):
                    update_quantity(product_name, price, 1)
                    st.rerun()
            
            with col2:
                if st.button(f"➖ {product_name}", key=f"remove_{product_name}", 
                           help="إزالة قطعة", type="secondary"):
                    update_quantity(product_name, price, -1)
                    st.rerun()
    
    else:
        st.info("🔍 لا توجد منتجات تطابق البحث المحدد")
    
    # Pagination Controls
    if total_pages > 1:
        st.markdown('<div class="pagination-container">', unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns([1, 1, 2, 1, 1])
        
        with col1:
            if st.button("⏮️ الأولى", disabled=st.session_state.current_page == 1):
                st.session_state.current_page = 1
                st.rerun()
        
        with col2:
            if st.button("⏪ السابقة", disabled=st.session_state.current_page == 1):
                st.session_state.current_page -= 1
                st.rerun()
        
        with col3:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.5rem; font-weight: 600;">
                صفحة {st.session_state.current_page} من {total_pages}
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.button("التالية ⏩", disabled=st.session_state.current_page == total_pages):
                st.session_state.current_page += 1
                st.rerun()
        
        with col5:
            if st.button("الأخيرة ⏭️", disabled=st.session_state.current_page == total_pages):
                st.session_state.current_page = total_pages
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # WhatsApp Order Button
    if st.session_state.cart:
        st.markdown("---")
        message = generate_whatsapp_message()
        whatsapp_number = st.secrets["whatsapp"]["number"]
        whatsapp_url = f"https://wa.me/{whatsapp_number}?text={urllib.parse.quote(message)}"
        
        st.markdown(f"""
        <div style="text-align: center; margin: 2rem 0;">
            <a href="{whatsapp_url}" target="_blank" class="whatsapp-btn">
                📱 إرسال الطلبية عبر واتساب
            </a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
