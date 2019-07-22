from django import forms
from .models import User

class userRegistration(forms.Form):

    # @汪同学， 我完全不知道怎么做 需要你的帮忙。简单的form我可以做 就是不知道怎么变
    # 得好看一些233 我把DB Table 还有 这个界面的代码做的和你接近了一些 希望能让你轻松点
    username = forms.CharField(label='Username: ', max_length=100)
    password = forms.CharField(label='Password: ', max_length=100)