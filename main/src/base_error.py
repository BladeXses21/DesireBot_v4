def on_cmd_error(ctx, error):
    if str(error) == 'not clan leader':
        return '***```Вы не лидер клана!```***'
    elif str(error) == 'not clan user':
        return '***```Вы не участник клана!```***'
