def is_admin(current_user):
    flag = False
    if (current_user.is_authenticated and current_user.id == 1):
        	flag = True
    if current_user.is_authenticated:
        print(current_user.id == 1, 'admin', current_user.username, 'access granted')
    return flag