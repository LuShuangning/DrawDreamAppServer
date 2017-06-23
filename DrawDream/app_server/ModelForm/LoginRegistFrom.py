from django import forms


class LoginFrom(forms.Form):
    username = forms.CharField(label='用户名：', max_length=100,
                               widget=forms.TextInput(
                                   attrs={'class': 'cont_form_login_username', "placeholder": "用户名"}),
                               error_messages={'required': '用户名不能为空'}, )
    password = forms.CharField(label='密码：', max_length="15", widget=forms.PasswordInput(
        attrs={'class': 'cont_form_login_password', "placeholder": "密码"}),
                               error_messages={'required': '密码不能为空'}, )


class RegistFrom(forms.Form):
    email = forms.EmailField(label='邮箱：', max_length=100,
                             widget=forms.TextInput(attrs={'class': 'cont_form_sign_up_email', "placeholder": "邮箱"}),
                             error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    username = forms.CharField(label='用户名：', max_length=100,
                               widget=forms.TextInput(attrs={'class': 'cont_form_sign_up_username', "placeholder": "用户名"}),
                               error_messages={'required': '用户名不能为空'}, )
    password = forms.CharField(label='密码：', max_length="15", widget=forms.PasswordInput(
        attrs={'class': 'cont_form_sign_up_password', "placeholder": "密码"}),
                               error_messages={'required': '密码不能为空'}, )
    re_password = forms.CharField(label='密码：', max_length="15", widget=forms.PasswordInput(
        attrs={'class': 'cont_form_sign_up_re_password', "placeholder": "确认密码"}),
                                  error_messages={'required': '不能为空'}, )
