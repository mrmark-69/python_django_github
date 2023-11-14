 select "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
 from "shopapp_product"
 where not "shopapp_product"."archived"
 order by "shopapp_product"."created_at" asc,
 "shopapp_product"."price" asc,
 "shopapp_product"."name" asc;

 select "django_session"."session_key",
    "django_session"."session_data",
    "django_session"."expire_date"
 from "django_session"
 where ("django_session"."expire_date" > '2023-11-06 12:20:42.487409'
 and "django_session"."session_key" = 'gxlmp24asai5x2np00y0ngfytq30334b')
 LIMIT 21; args=('2023-11-06 12:20:42.487409', 'gxlmp24asai5x2np00y0ngfytq30334b');

 select "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
 from "auth_user"
 where "auth_user"."id" = 2
 LIMIT 21;

select "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
from "shopapp_product"
where "shopapp_product"."id" = 29 LIMIT 21;

select "shopapp_productimage"."id",
    "shopapp_productimage"."product_id", "
    shopapp_productimage"."image",
    "shopapp_productimage"."description"
from "shopapp_productimage"
where "shopapp_productimage"."product_id" in (29);

select "django_session"."session_key",
    "django_session"."session_data",
    "django_session"."expire_date"
from "django_session"
where ("django_session"."expire_date" > '2023-11-06 12:34:01.924034'
and "django_session"."session_key" = 'gxlmp24asai5x2np00y0ngfytq30334b')
LIMIT 21; args=('2023-11-06 12:34:01.924034', 'gxlmp24asai5x2np00y0ngfytq30334b');

select "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
from "auth_user"
where "auth_user"."id" = 2 LIMIT 21;

select "shopapp_order"."id",
    "shopapp_order"."delivery_address",
    "shopapp_order"."promocode",
    "shopapp_order"."created_at",
    "shopapp_order"."user_id",
    "shopapp_order"."receipt",
    "auth_user"."id",
    "auth_user"."password",
    "auth_user"."last_login",
    "auth_user"."is_superuser",
    "auth_user"."username",
    "auth_user"."first_name",
    "auth_user"."last_name",
    "auth_user"."email",
    "auth_user"."is_staff",
    "auth_user"."is_active",
    "auth_user"."date_joined"
from "shopapp_order" inner join "auth_user" on ("shopapp_order"."user_id" = "auth_user"."id");

select ("shopapp_order_products"."order_id") as "_prefetch_related_val_order_id",
    "shopapp_product"."id",
    "shopapp_product"."name",
    "shopapp_product"."description",
    "shopapp_product"."price",
    "shopapp_product"."discount",
    "shopapp_product"."created_at",
    "shopapp_product"."archived",
    "shopapp_product"."created_by_id",
    "shopapp_product"."preview"
from "shopapp_product" inner join "shopapp_order_products"
on ("shopapp_product"."id" = "shopapp_order_products"."product_id")
where "shopapp_order_products"."order_id" in (2, 3, 4)
order by "shopapp_product"."created_at" asc, "shopapp_product"."price" asc, "shopapp_product"."name" asc;

