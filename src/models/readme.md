sqlachemy(sync):
- 增：add()、add_all()
- 删：delete()
- 改：update()
- 查：query()
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

sqlalchemy(async): 目前使用的是sqlalchemy.ext.asyncio.async_scoped_session <- session
- 增：add()、add_all()
- 删：delete()
- 改：
- 查：
    -- get() 根据给定的主键标识返回一个实例，没有返回None  （获取单个实例的时候推荐使用）
    -- scalar() 执行语句并返回标量(实例对象),但是只能查到第一个
    -- execute() 执行一条语句并返回一个缓冲Result对象  (不能直接在缓冲对象上面直接执行下列的方法，只能先将其赋值之后再操作)
        -- all() 返回列表中的所有行（调用后清空）
        -- fetchmany() 获取多行（调用后清空）
        -- fetchone() 获取一行（调用后清空）
        -- first() 获取第一行，没有返回None
        -- scalar() 获取第一行的第一列（调用后清空）
        -- scalars() 获取所有行的第一列，以列表的方式返回（调用后清空）


sqlalchemy提供生成sql语句的所有方法：
"Alias",
    "AliasedReturnsRows",
    "any_",
    "all_",
    "CacheKey",
    "ClauseElement",
    "ColumnCollection",
    "ColumnElement",
    "CompoundSelect",
    "Delete",
    "FromClause",
    "Insert",
    "Join",
    "Lateral",
    "LambdaElement",
    "StatementLambdaElement",
    "Select",
    "Selectable",
    "TableClause",
    "TableValuedAlias",
    "Update",
    "Values",
    "alias",
    "and_",
    "asc",
    "between",
    "bindparam",
    "case",
    "cast",
    "column",
    "custom_op",
    "cte",
    "delete",
    "desc",
    "distinct",
    "except_",
    "except_all",
    "exists",
    "extract",
    "func",
    "modifier",
    "collate",
    "insert",
    "intersect",
    "intersect_all",
    "join",
    "label",
    "lateral",
    "lambda_stmt",
    "literal",
    "literal_column",
    "not_",
    "null",
    "nulls_first",
    "nulls_last",
    "or_",
    "outparam",
    "outerjoin",
    "over",
    "select",
    "table",
    "text",
    "tuple_",
    "type_coerce",
    "quoted_name",
    "union",
    "union_all",
    "update",
    "quoted_name",
    "within_group",
    "Subquery",
    "TableSample",
    "tablesample",
    "values",
