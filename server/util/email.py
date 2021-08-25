from django.core.mail import EmailMessage
from typing import Optional, List
from django.template.loader import render_to_string


def send_email(subject: str, body: str, to: List[str],
               filepath: Optional[List[str]] = None,
               cc: Optional[List[str]] = None,
               html=False, template: Optional[str] = None,
               data: Optional[dict] = None):
    """
    :param subject: 邮件主题
    :param body: 邮件正文内容
    :param to: 接受方
    :param filepath: 附件 list 可以是文件也可以是图片路径
    :param cc: 抄送
    :param html: 是否发送html格式邮件内容
    :param template: 渲染的html模板路径
    :param data: 渲染html的数据
    :return:
    """

    # 注意 如果要渲染html模板 需要在setting中配置 template路径 渲染template
    """
    TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], 渲染模板放在templates文件夹中
    """
    if html:
        body = render_to_string(template, data)

    msg = EmailMessage(
        subject=subject,
        body=body,
        from_email=None,  # 默认获取settings中的DEFAULT_FROM_EMAIL
        to=to,
        cc=cc
    )
    if filepath:
        for file in filepath:
            msg.attach_file(file)
    if html:
        msg.content_subtype = 'html'
    code = msg.send(fail_silently=False)
    return code
