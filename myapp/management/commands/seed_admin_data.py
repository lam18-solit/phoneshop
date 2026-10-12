import random
import uuid
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from myapp.models import CustomUser, Product, OrderTracking, Review, Category, Company


class Command(BaseCommand):
    help = 'Seed demo orders, customers, and reviews for Admin Dashboard'

    def handle(self, *args, **kwargs):
        self.stdout.write('Checking and seeding demo data...')

        # 1. Create or get Admin user
        admin_user, created = CustomUser.objects.get_or_create(
            email='admin@phoneshop.com',
            defaults={
                'first_name': 'Quản Trị',
                'last_name': 'Viên',
                'phone': '0988889999',
                'address': 'Showroom Phone Shop, Đà Nẵng',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123456')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user: admin@phoneshop.com / admin123456'))
        else:
            if not admin_user.is_staff or not admin_user.is_superuser:
                admin_user.is_staff = True
                admin_user.is_superuser = True
                admin_user.save()
            self.stdout.write('Admin user admin@phoneshop.com already exists.')

        # Also ensure lam181204@gmail.com is staff & superuser
        lam_user = CustomUser.objects.filter(email='lam181204@gmail.com').first()
        if lam_user:
            lam_user.is_staff = True
            lam_user.is_superuser = True
            lam_user.save()

        # 2. Create demo customers
        sample_customers = [
            {'email': 'nguyenvana@gmail.com', 'first': 'Văn A', 'last': 'Nguyễn', 'phone': '0905123456', 'address': '123 Lê Duẩn, Hải Châu, Đà Nẵng'},
            {'email': 'tranthib@gmail.com', 'first': 'Thị B', 'last': 'Trần', 'phone': '0912345678', 'address': '45 Nguyễn Thị Minh Khai, Q.1, TP.HCM'},
            {'email': 'lehoangc@gmail.com', 'first': 'Hoàng C', 'last': 'Lê', 'phone': '0987654321', 'address': '78 Cầu Giấy, Hà Nội'},
            {'email': 'phamthid@gmail.com', 'first': 'Thị D', 'last': 'Phạm', 'phone': '0935112233', 'address': '12 Bạch Đằng, Hải Châu, Đà Nẵng'},
            {'email': 'hoangvane@gmail.com', 'first': 'Văn E', 'last': 'Hoàng', 'phone': '0978998877', 'address': '99 Trần Phú, Nha Trang'},
        ]

        created_users = [admin_user]
        for c in sample_customers:
            u, c_created = CustomUser.objects.get_or_create(
                email=c['email'],
                defaults={
                    'first_name': c['first'],
                    'last_name': c['last'],
                    'phone': c['phone'],
                    'address': c['address'],
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            if c_created:
                u.set_password('customer123')
                u.save()
            created_users.append(u)

        products = list(Product.objects.filter(is_active=True))
        if not products:
            self.stdout.write(self.style.WARNING('No active products found to seed orders.'))
            return

        # 3. Seed demo orders if none exist
        if OrderTracking.objects.count() == 0:
            self.stdout.write('Seeding demo orders...')
            # Choices: (2, 'Placed'), (3, 'Shipped'), (4, 'Delivered'), (5, 'Cancelled')
            status_choices = [2, 3, 4, 4, 4, 5]
            now = timezone.now()

            # Generate 18 realistic orders
            for i in range(18):
                user = random.choice(created_users[1:])  # pick customers
                product = random.choice(products)
                qty = random.choice([1, 1, 1, 2])
                price = product.discounted_price() if product.discount_percentage > 0 else product.orignal_price
                if price <= 0:
                    price = 15990000
                total_amount = price * qty
                order_st = random.choice(status_choices)

                # Spread dates over past 30 days
                days_ago = random.randint(0, 28)
                created_dt = now - timedelta(days=days_ago, hours=random.randint(1, 12))

                order = OrderTracking(
                    order_id=f"ORD{1000 + i}{random.randint(10, 99)}",
                    user=user,
                    product=product,
                    quantity=qty,
                    total_price=total_amount,
                    order_status=order_st,
                )
                order.save()
                # Overwrite auto_now_add for realistic spread
                OrderTracking.objects.filter(id=order.id).update(created_at=created_dt)

            self.stdout.write(self.style.SUCCESS(f'Created {OrderTracking.objects.count()} demo orders.'))
        else:
            self.stdout.write(f'Existing orders count: {OrderTracking.objects.count()}')

        # 4. Seed demo reviews if none exist
        if Review.objects.count() == 0:
            self.stdout.write('Seeding demo reviews...')
            review_samples = [
                ('Sản phẩm tuyệt vời!', 'Điện thoại dùng rất mượt, pin trâu, camera chụp hình cực nét. Đóng gói cẩn thận và giao hàng siêu nhanh!', 5),
                ('Rất đáng tiền', 'Máy chính hãng mới nguyên seal 100%, bảo hành chuẩn. Shop tư vấn nhiệt tình, sẽ ủng hộ tiếp!', 5),
                ('Hài lòng trong tầm giá', 'Thiết kế đẹp mắt, cầm chắc tay. Hiệu năng ổn định khi chơi game và lướt web.', 4),
                ('Giao hàng nhanh', 'Đặt hôm qua hôm nay đã nhận được hàng. Máy chạy mát, phụ kiện đi kèm đầy đủ.', 5),
                ('Chất lượng tốt', 'Màn hình sắc nét, độ sáng cao ngoài trời nhìn rõ. Rất hài lòng với quyết định mua máy này.', 4),
            ]
            for i, p in enumerate(products[:8]):
                sample = review_samples[i % len(review_samples)]
                user = random.choice(created_users[1:])
                Review.objects.create(
                    product=p,
                    user=user,
                    name=f"{user.last_name} {user.first_name}",
                    title=sample[0],
                    review=sample[1],
                    rating=sample[2]
                )
            self.stdout.write(self.style.SUCCESS(f'Created {Review.objects.count()} demo reviews.'))

        self.stdout.write(self.style.SUCCESS('Demo data seeding completed successfully!'))
