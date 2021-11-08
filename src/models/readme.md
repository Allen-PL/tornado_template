sqlachemy:
- 增：add()、add_all()
- 删：delete()
- 改：update()
- 查：query
    -- first(): 返回标量，没有返回None
    -- one(): 返回标量，没有报错
    -- scalar(): 返回变量，没有返回None
    -- filter_by(text("id>1")): 未commit，懒加载
    -- filter(Table.id=1): 未commit，懒加载
    -- all(): 返回列表
    -- order_by(): 返回列表
    -- text(): 执行原生sql
    -- params(): 配合text传递给原生语句参数
    -- exists(): 是否存在
    -- group_by(): 分组
    -- join(): 关联

