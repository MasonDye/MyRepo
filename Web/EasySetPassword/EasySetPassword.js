let password = 123456//Setting Password
let inputPassword = prompt("Please input password")//Input password
while (inputpassword != password)//If input password not right then while
{
    alert("You input password not right")//Tips password not right
    inputPassword = prompt("Please again input password")//Again input password
}
alert("You input password is a right")//If password right then run