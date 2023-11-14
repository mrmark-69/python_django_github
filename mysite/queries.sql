                            SELECT "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview"
                                    FROM "shopapp_product"
                                    WHERE NOT "shopapp_product"."archived"
                                    ORDER BY "shopapp_product"."created_at" ASC, "shopapp_product"."price" ASC, "shopapp_product"."name" ASC;
                            SELECT "django_session"."session_key", "django_session"."session_data", "django_session"."expire_date"
                                    FROM "django_session"
                                    WHERE ("django_session"."expire_date"> '2023-11-14 00:37:18.702642' AND "django_session"."session_key" = 'gxlmp24asai5x2np00y0ngfytq30334b') LIMIT 21 ; args = ('2023-11-14 00:37:18.702642', 'gxlmp24asai5x2np00y0ngfytq30334b') ;
                            SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined"
                                    FROM "auth_user"
                                    WHERE "auth_user"."id" = 2 LIMIT 21 ;


                            SELECT "shopapp_product"."id", "shopapp_product"."name", "shopapp_product"."description", "shopapp_product"."price", "shopapp_product"."discount", "shopapp_product"."created_at", "shopapp_product"."archived", "shopapp_product"."created_by_id", "shopapp_product"."preview"
                                    FROM "shopapp_product"
                                    WHERE "shopapp_product"."id" = 29 LIMIT 21 ;
                            SELECT "shopapp_productimage"."id", "shopapp_productimage"."product_id", "shopapp_productimage"."image", "shopapp_productimage"."description"
                                    FROM "shopapp_productimage"
                                    WHERE "shopapp_productimage"."product_id" IN (29);
                            SELECT "auth_user"."id", "auth_user"."password", "auth_user"."last_login", "auth_user"."is_superuser", "auth_user"."username", "auth_user"."first_name", "auth_user"."last_name", "auth_user"."email", "auth_user"."is_staff", "auth_user"."is_active", "auth_user"."date_joined"
                                    FROM "auth_user"
                                    WHERE "auth_user"."id" = 1 LIMIT 21 ;

                            SELECT "blogapp_article"."id", "blogapp_article"."title", "blogapp_article"."content", "blogapp_article"."pub_date", "blogapp_article"."author_id", "blogapp_article"."category_id", "blogapp_author"."id", "blogapp_author"."name", "blogapp_author"."bio", "blogapp_category"."id", "blogapp_category"."name"
                                    FROM "blogapp_article" LEFT OUTER JOIN "blogapp_author" ON ("blogapp_article"."author_id" = "blogapp_author"."id") LEFT OUTER JOIN "blogapp_category" ON ("blogapp_article"."category_id" = "blogapp_category"."id");

