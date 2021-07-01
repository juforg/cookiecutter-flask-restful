# -*- coding: utf-8 -*-
# @author: songjie@shanshu.ai
# @date: 2019/11/08

from {{cookiecutter.app_name}}.commons.exception import C
"""状态码枚举类
usage：
    结构为：错误枚举名-错误码code-错误说明msg
"""


SUCCESS = C(200000, "成功")
NO_RESULT = C(200001, "未生成任务")

# 权限类
LOGIN_EXPIRED = C(300001, "登录过期")
INVALID_TOKEN = C(300002, "令牌无效")
INVALID_SIGNATURE = C(300003, "签名无效")

# 请求参数类
PARAM_IS_NULL = C(400001, "请求参数为空")
JSON_PARSE_FAIL = C(400002, "JSON转换失败")
PARAM_ILLEGAL = C(400003, "请求参数非法")
PAGE_NOT_FOUND = C(400004, "页面不存在")
METHOD_NOT_ALLOWED = C(400005, "方法不允许")
REPEATED_COMMIT = C(400006, "重复提交")
USER_NOT_FOUND = C(400007, "用户不存在")
NAME_PWD_INVALID = C(400008, "用户名或密码错误")
NOT_FOUND = C(400009, "资源为找到")
ALREADY_EXIST = C(400010, "资源已存在")
# 技术类
UNKNOWN_ERROR = C(500000, "未知异常")
SQL_ERROR = C(510000, "数据库异常")

# 业务类
# # 警告类⚠️

W_LOC_NOT_IN_DM_ZG = C(6100, "库位不在距离矩阵中或不在本库区中，算法将无法使用其库存或库容或在其位置上的叉车:[{}]")
W_AVAIL_DC_NOT_IN_DM = C(6101, "可用码头不在距离矩阵中或不在本库区中:[{}]")
W_NO_CURR_FORKLIFT_VEH = C(6102, "无可用叉车实时数据")
W_TASK_INFO_NOT_ENOUGH = C(6103, "任务的起点、终点、任务类型、起点终点对应工作区zpick等信息为空无法指派")
W_TASK_EXPIRED = C(6104, "任务长时间未执行超期")
W_NO_INV_DATA = C(6105, "无库存数据，无需理货")

# # 数据问题
D_NO_PRODUCTION_LINE = C(6200, "无相关产线主数据")
D_DATE_FORMAT_ERROR = C(6201, "日期格式有问题")
D_NO_ALGO_PARAMS = C(6202, "算法参数集为空,warehouse_id:{}, zone_group:{}")
D_LOC_NOT_IN_DM = C(6203, "库位码不在距离矩阵中")
D_IN_NOT_BATCH = C(6204, "入库没批次信息")
D_SKU_MATCH_ERROR = C(6205, "任务池sku与产品主数据中sku匹配不上")
D_BATCH_FROMAT_ERROR = C(6206, "批次:[{}],格式不合法")
D_NO_DEPOT_LOC = C(6207, "无库位数据(库位主数据中不存在可上架该订单的库位)")
D_CROSS_DOCK_NOT_IN_DM = C(6209, "越库码头不存在库位主数据中cross_dock,][分割:[{}]")
D_AVAILABLE_DOCK_NOT_IN_DM = C(6210, "可用码头没有一个存在距离矩阵中:[{}]")
D_NO_DOCK_DICT = C(6211, "无码头数据")
D_NO_MATERIAL = C(6212, "无相关产品主数据")
D_NO_BIN_DOCK_REL = C(6213, "无该仓库库位码头关系数据")
D_ORDER_POINT_NOT_IN_DM = C(6214, "该订单的起点或终点:[{}]不在距离矩阵中")
D_NO_SKU = C(6215, "产品[{}]不在产品主数据中")
D_LINE_BIN_NOT_IN_DM = C(6216, "产线的线边库[{}]不在距离矩阵中")
D_NO_ALGO_SPECIFIC_PARAM = C(6217, "未配置算法参数param_module:[{}]_param_name:[{}]")
D_ALGO_PARAM_FORMAT_ERROR = C(6218, "配置参数param_module:[{}]_param_name:[{}]不合法")

# 距离矩阵计算相关
D_CONFLICT_LOCATION_DATA = C(6220, "{}个位置有不一致的数据信息，包含: {}")
D_NO_LANE_DATA_LOCATION = C(6221, "{}个库位的所属巷道号没有数据: {}")
D_NO_LOC_DIRECTION = C(6222, "{}个{}的loc_direction不在{}范围内: {}")
# 码头指派计算相关
D_MULTI_APPOINTED_DOCK_ERROR = C(6223, "存在{}个指定码头信息: {}")
D_APPOINTED_DOCK_NOT_IN_MATRIX = C(6224, "订单中的指定码头[{}]不在距离矩阵中。")
D_PRODUCTION_LINE_ERROR = C(6225, "对于sku[{}]，有直发需求但直发产线[{}]不在产线主数据中")
D_IN_NO_BATCH_ID = C(6226, "sku[{}]无批次信息，无法做入库判断")
D_LOC_NO_DOCK = C(6227, "在多码头的场景下，库位[{}]没有可达码头")
# 布局优化相关
D_LOC_NO_SKU_GROUP = C(6228, "库位{}的库容信息不全。没有以下sku group的库容: {}")
D_NO_PRODUCTION_PLAN = C(6229, "无生产计划数据")
D_NO_FUTURE_ORDER = C(6230, "无未来订单数据")
# # 业务问题
B_OUT_INV_NOT_ENOUGH = C(6300, "出库sku库存不足,order_id:{}, sku:{}, batch:{}, 需求量:{}, 实际可达可用量:{}")
B_IN_SPACE_NOT_ENOUGH = C(6301, "入库sku库存空间不足,order_id:{}, sku:{}, batch:{}, 需求量:{}, 实际可存入量:{}")
B_WP_NOT_ENOUGH = C(6301, "出库的时候移库没有地方存（散箱拣货移库收货库位不可用）")
B_RERUN_ID_NOT_FOUND = C(6302, "未找到对应taskId重算重建任务")
# B_OUT_NO_DEST = C(6303, "出库订单没有终点") 合并到 6214
# B_IN_NO_ORIGIN = C(6304, "入库订单没有起点")
B_NO_ENGOUTH_LOC = C(6305, "入库可达库位库存空间不足,所有可达库位ID:[{}]")
# IN_ = C(6306, "入库常规货架无可用库位")
# IN_ = C(6307, "入库尾数架无可用库位")
B_CAL_DOCK_ERROR = C(6308, "码头指派计算结果异常！库位送达的码头：{}，实际选择的码头：{}")
B_NO_DOCKS = C(6309, "码头指派计算无可行解")
B_NO_LAYOUT = C(6310, "布局优化计算无可行解")

# 第三方系统类


if __name__ == '__main__':
    try:
        error = W_LOC_NOT_IN_DM_ZG.f("test", "sadf", "s11111")
        raise error
    except C as c:
        print(c.code)
        print(c.msg)
        print(c)
