import json
import os
from pathlib import Path
from django.conf import settings

DATA_DIR = Path(settings.BASE_DIR) / 'project'

COUPONS_FILE = DATA_DIR / 'store_coupons.json'
SETTINGS_FILE = DATA_DIR / 'store_settings.json'

DEFAULT_COUPONS = [
    {
        'id': 1,
        'code': 'PHONESHOP10',
        'discount_type': 'percent',
        'discount_value': 10,
        'min_spend': 5000000,
        'usage_limit': 100,
        'used_count': 23,
        'valid_until': '2026-12-31',
        'is_active': True,
        'description': 'Giảm 10% cho đơn hàng điện thoại từ 5 triệu'
    },
    {
        'id': 2,
        'code': 'IPHONEVIP',
        'discount_type': 'fixed',
        'discount_value': 1000000,
        'min_spend': 20000000,
        'usage_limit': 50,
        'used_count': 12,
        'valid_until': '2026-11-30',
        'is_active': True,
        'description': 'Giảm ngay 1.000.000 ₫ cho dòng iPhone cao cấp'
    },
    {
        'id': 3,
        'code': 'FREESHIP50',
        'discount_type': 'fixed',
        'discount_value': 50000,
        'min_spend': 2000000,
        'usage_limit': 200,
        'used_count': 84,
        'valid_until': '2026-12-31',
        'is_active': True,
        'description': 'Miễn phí giao hàng toàn quốc đơn từ 2 triệu'
    },
    {
        'id': 4,
        'code': 'SAMSUNG20',
        'discount_type': 'percent',
        'discount_value': 15,
        'min_spend': 8000000,
        'usage_limit': 30,
        'used_count': 30,
        'valid_until': '2026-10-31',
        'is_active': False,
        'description': 'Ưu đãi 15% mùa tựu trường cho dòng Galaxy'
    }
]

DEFAULT_SETTINGS = {
    'store_name': 'Phone Shop - Lam Shop',
    'tagline': 'Trao quyền cho cuộc sống công nghệ!',
    'hotline': '0988 889 999',
    'support_email': 'support@phoneshop.com',
    'address': 'Showroom Phone Shop, Quận Hải Châu, TP. Đà Nẵng',
    'currency': 'VND',
    'currency_symbol': '₫',
    'announcement_bar': '🔥 KHUYẾN MÃI ĐẶC BIỆT: Giảm ngay 1.000.000 ₫ khi mua iPhone 15 Pro & Tặng ốp lưng cao cấp!',
    'is_announcement_active': True,
    'maintenance_mode': False,
    'free_shipping_threshold': 5000000,
    'facebook_url': 'https://facebook.com/phoneshop',
    'zalo_phone': '0988889999',
}


def get_coupons():
    if not COUPONS_FILE.exists():
        save_coupons(DEFAULT_COUPONS)
        return DEFAULT_COUPONS
    try:
        with open(COUPONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_COUPONS


def save_coupons(coupons):
    try:
        with open(COUPONS_FILE, 'w', encoding='utf-8') as f:
            json.dump(coupons, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving coupons: {e}")


def get_settings():
    if not SETTINGS_FILE.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS
    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            merged = {**DEFAULT_SETTINGS, **data}
            return merged
    except Exception:
        return DEFAULT_SETTINGS


def save_settings(settings_data):
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(settings_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving settings: {e}")
