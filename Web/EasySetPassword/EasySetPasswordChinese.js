let password = 123456//设置密码
inputPassword = prompt("Please input password")//输入密码
while (inputPassword != password)//如果输入的密码不正确则进入循环节
{
    alert("You input password not right")//提示密码不正确
    inputPassword = prompt("Please again input password")//再次输入密码
}
alert("You input password is a right")//如果密码正确则执行