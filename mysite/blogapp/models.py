from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField()

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    name = models.CharField(max_length=40, )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    pub_date = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(Tag, related_name='articles')
