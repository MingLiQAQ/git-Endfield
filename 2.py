import pandas as pd
from itertools import combinations
import os

# ==================== 参数配置区域 ====================
# 用户可以在这里直接修改参数，无需交互式输入

# 目标武器名称 (输入要查询的武器名称，例如: "宏愿")
TARGET_WEAPON = "热熔切割器"

# 是否在输出结果中显示武器星级
SHOW_STAR = 1

# 最低显示武器星级 (4, 5, 6)
MIN_STAR =5

# 是否在输出结果中显示武器类型，1 = Ture ,0 = False
SHOW_TYPE = 0


# ==================== 参数配置结束 ====================

class WeaponAnalysis:
    def __init__(self, excel_path, target_weapon=None, show_star=True, min_star=5, show_type=True):
        """初始化，读取所有sheet的数据"""
        self.excel_path = excel_path

        # 参数验证和设置
        self.target_weapon = target_weapon
        self.show_star = bool(show_star)
        self.min_star = int(min_star)
        self.show_type = bool(show_type)

        # 参数范围验证
        if self.min_star not in [4, 5, 6]:
            print(f"警告: 最小星级{self.min_star}无效，使用默认值5")
            self.min_star = 5

        self.weapons_df = None
        self.maps_data = {}
        self.load_data()

    def load_data(self):
        """从Excel文件加载数据 - 自动检测地图表"""
        try:
            # 读取武器信息表（Sheet1）
            self.weapons_df = pd.read_excel(self.excel_path, sheet_name='Sheet1')
            print(f"成功加载武器数据: {len(self.weapons_df)} 件武器")

            # 自动检测所有sheet，排除Sheet1
            xls = pd.ExcelFile(self.excel_path)
            all_sheets = xls.sheet_names

            # 找出所有地图表（排除Sheet1）
            map_sheets = [sheet for sheet in all_sheets if sheet != 'Sheet1']

            if not map_sheets:
                print("警告: 未找到任何地图表!")
                return

            print(f"检测到 {len(map_sheets)} 个地图表: {', '.join(map_sheets)}")

            for map_name in map_sheets:
                try:
                    df = pd.read_excel(self.excel_path, sheet_name=map_name)

                    # 检查必要的列是否存在
                    required_columns = ['第一词条', '第二词条', '第三词条']
                    missing_columns = [col for col in required_columns if col not in df.columns]

                    if missing_columns:
                        print(f"  警告: 地图 {map_name} 缺少列: {missing_columns}，跳过")
                        continue

                    # 清理数据
                    df_clean = df.dropna(subset=required_columns, how='all')
                    self.maps_data[map_name] = df_clean

                    # 统计信息
                    first_count = df_clean['第一词条'].dropna().count()
                    second_count = df_clean['第二词条'].dropna().count()
                    third_count = df_clean['第三词条'].dropna().count()

                    # print(f"  成功加载地图: {map_name} ({len(df_clean)}行)")
                    # print(f"    第一词条: {first_count}种，第二词条: {second_count}种，第三词条: {third_count}种")

                except Exception as e:
                    print(f"  错误: 加载地图 {map_name} 失败: {str(e)}")

        except Exception as e:
            print(f"错误: 加载Excel文件失败: {str(e)}")
            raise

    def get_weapon_info(self, weapon_name):
        """获取指定武器的信息"""
        weapon_row = self.weapons_df[self.weapons_df['武器名称'] == weapon_name]
        if weapon_row.empty:
            return None

        weapon = weapon_row.iloc[0]
        return {
            '名称': weapon['武器名称'],
            '第一词条': weapon['第一词条'],
            '第二词条': weapon['第二词条'],
            '第三词条': weapon['第三词条'],
            '类型': weapon['武器类型'],
            '星级': weapon['武器星级']
        }

    def can_drop_in_map(self, weapon_info, map_name):
        """检查武器是否可在指定地图掉落"""
        if map_name not in self.maps_data:
            return False

        map_df = self.maps_data[map_name]

        # 检查所有三个词条是否都出现在地图中
        first_in_map = weapon_info['第一词条'] in map_df['第一词条'].dropna().tolist()
        second_in_map = weapon_info['第二词条'] in map_df['第二词条'].dropna().tolist()
        third_in_map = weapon_info['第三词条'] in map_df['第三词条'].dropna().tolist()

        return first_in_map and second_in_map and third_in_map

    def find_droppable_maps(self, weapon_info):
        """找出武器可掉落的地图（所有词条都匹配的地图）"""
        droppable_maps = []

        for map_name in self.maps_data.keys():
            if self.can_drop_in_map(weapon_info, map_name):
                droppable_maps.append(map_name)

        return droppable_maps

    def get_str_width(self, s):
        """计算字符串在终端中的显示宽度（考虑中文字符）"""
        width = 0
        for char in s:
            # 中文字符通常占2个字符宽度
            if '\u4e00' <= char <= '\u9fff':
                width += 2
            else:
                width += 1
        return width

    def format_combo(self, combo):
        """格式化第一词条组合，移除'提升'二字"""
        simplified = []
        for trait in combo:
            if trait.endswith('提升'):
                simplified.append(trait[:-2])
            else:
                simplified.append(trait)
        return "+".join(simplified)

    def format_weapon_display(self, weapon_name, weapon_type, weapon_star):
        """格式化武器显示信息，包括星级和类型"""
        # 检查是否满足最低星级要求
        if weapon_star < self.min_star:
            return None  # 不显示此武器

        parts = []

        if self.show_star:
            parts.append(f"{weapon_star}星")

        if self.show_type:
            parts.append(weapon_type)

        if parts:
            return f"{weapon_name}（{' '.join(parts)}）"
        else:
            return weapon_name

    def sort_weapons_by_star(self, weapons_list):
        """按星级对武器列表进行排序（高星在前）"""
        # 获取武器信息并过滤
        weapons_with_info = []
        for weapon_name in weapons_list:
            weapon_info = self.get_weapon_info(weapon_name)
            if weapon_info:
                formatted = self.format_weapon_display(
                    weapon_info['名称'],
                    weapon_info['类型'],
                    weapon_info['星级']
                )
                if formatted:  # 不为None表示满足最低星级
                    weapons_with_info.append({
                        'display': formatted,
                        'star': weapon_info['星级'],
                        'name': weapon_info['名称']
                    })

        # 按星级降序排序，同星级按名称排序
        sorted_weapons = sorted(
            weapons_with_info,
            key=lambda x: (-x['star'], x['name'])
        )

        # 提取显示字符串
        return [weapon['display'] for weapon in sorted_weapons]

    def analyze_weapon(self, target_weapon_name=None):
        """分析目标武器的刷取组合"""
        if target_weapon_name is None:
            target_weapon_name = self.target_weapon

        # 获取目标武器信息
        target_info = self.get_weapon_info(target_weapon_name)
        if not target_info:
            print(f"未找到武器: {target_weapon_name}")
            return

        print(f"\n分析目标武器: {target_info['名称']}")
        print(f"武器信息: {target_info['第一词条']} | {target_info['第二词条']} | {target_info['第三词条']}")
        print(f"武器类型: {target_info['类型']} | 星级: {target_info['星级']}")
        print("-" * 60)

        # 找出可掉落的地图（所有词条都匹配）
        droppable_maps = self.find_droppable_maps(target_info)

        if not droppable_maps:
            print(f"警告: {target_info['名称']} 在所有地图都无法掉落（词条不完整匹配）")
            return

        print(f"可在以下 {len(droppable_maps)} 个地图刷取: {', '.join(droppable_maps)}")

        for map_name in droppable_maps:
            print(f"\n【{map_name}】")

            map_df = self.maps_data[map_name]
            first_options = map_df['第一词条'].dropna().unique().tolist()

            # 目标武器的第一词条必须被选中
            if target_info['第一词条'] not in first_options:
                print(f"  警告: 地图 {map_name} 不包含目标武器的第一词条")
                continue

            # 从剩下的第一词条中选2个
            other_first = [f for f in first_options if f != target_info['第一词条']]

            if len(other_first) < 2:
                print(f"  警告: 地图 {map_name} 的第一词条不足，无法形成组合")
                continue

            # 生成所有可能的组合
            combinations_list = list(combinations(other_first, 2))
            # print(f"  可能的词条组合数: {len(combinations_list)}")

            # 分析固定第二词条的情况
            has_second = self.analyze_fixed_second(map_name, first_options, target_info, combinations_list)

            # 分析固定第三词条的情况
            has_third = self.analyze_fixed_third(map_name, first_options, target_info, combinations_list)

            if not has_second and not has_third:
                print("  无符合条件的其他武器")

    def analyze_fixed_second(self, map_name, map_first_options, target_info, combinations_list):
        """分析固定第二词条的情况"""
        map_df = self.maps_data[map_name]
        second_options = map_df['第二词条'].dropna().unique().tolist()

        # 检查目标武器的第二词条是否在地图的第二词条选项中
        if target_info['第二词条'] not in second_options:
            return False

        has_output = False

        # 对于每个第一词条组合
        for combo in combinations_list:
            selected_first = list(combo) + [target_info['第一词条']]

            # 找出符合条件的其他武器
            compatible_weapons = []

            for _, weapon in self.weapons_df.iterrows():
                # 排除目标武器自身
                if weapon['武器名称'] == target_info['名称']:
                    continue

                # 检查条件
                weapon_info = {
                    '名称': weapon['武器名称'],
                    '第一词条': weapon['第一词条'],
                    '第二词条': weapon['第二词条'],
                    '第三词条': weapon['第三词条']
                }

                if (weapon['第一词条'] in selected_first and
                        weapon['第二词条'] == target_info['第二词条'] and
                        self.can_drop_in_map(weapon_info, map_name)):
                    compatible_weapons.append(weapon['武器名称'])

            if compatible_weapons:
                has_output = True
                # 格式化输出
                combo_str = self.format_combo(combo)
                combo_width = self.get_str_width(combo_str)
                target_width = 15

                if combo_width < target_width:
                    spaces_needed = target_width - combo_width
                    aligned_combo = combo_str + " " * spaces_needed
                else:
                    aligned_combo = combo_str

                # 对武器列表按星级排序并格式化显示
                sorted_weapons = self.sort_weapons_by_star(compatible_weapons)

                if sorted_weapons:  # 可能有武器因星级过滤而不显示
                    print(f"  {aligned_combo}\t{target_info['第二词条']}: {', '.join(sorted_weapons)}")

        return has_output

    def analyze_fixed_third(self, map_name, map_first_options, target_info, combinations_list):
        """分析固定第三词条的情况"""
        map_df = self.maps_data[map_name]
        third_options = map_df['第三词条'].dropna().unique().tolist()

        # 检查目标武器的第三词条是否在地图的第三词条选项中
        if target_info['第三词条'] not in third_options:
            return False

        has_output = False

        # 对于每个第一词条组合
        for combo in combinations_list:
            selected_first = list(combo) + [target_info['第一词条']]

            # 找出符合条件的其他武器
            compatible_weapons = []

            for _, weapon in self.weapons_df.iterrows():
                # 排除目标武器自身
                if weapon['武器名称'] == target_info['名称']:
                    continue

                # 检查条件
                weapon_info = {
                    '名称': weapon['武器名称'],
                    '第一词条': weapon['第一词条'],
                    '第二词条': weapon['第二词条'],
                    '第三词条': weapon['第三词条']
                }

                if (weapon['第一词条'] in selected_first and
                        weapon['第三词条'] == target_info['第三词条'] and
                        self.can_drop_in_map(weapon_info, map_name)):
                    compatible_weapons.append(weapon['武器名称'])

            if compatible_weapons:
                has_output = True
                # 格式化输出
                combo_str = self.format_combo(combo)
                combo_width = self.get_str_width(combo_str)
                target_width = 15

                if combo_width < target_width:
                    spaces_needed = target_width - combo_width
                    aligned_combo = combo_str + " " * spaces_needed
                else:
                    aligned_combo = combo_str

                # 对武器列表按星级排序并格式化显示
                sorted_weapons = self.sort_weapons_by_star(compatible_weapons)

                if sorted_weapons:  # 可能有武器因星级过滤而不显示
                    print(f"  {aligned_combo}\t{target_info['第三词条']}: {', '.join(sorted_weapons)}")

        return has_output


def main():
    # 获取当前目录下的Excel文件
    excel_file = "武器毕业基质表.xlsx"

    if not os.path.exists(excel_file):
        print(f"错误: 找不到文件 {excel_file}")
        print("请确保Excel文件与脚本在同一目录下")
        return

    # print("=" * 60)
    print("武器刷取分析工具")
    # print("=" * 60)
    print(f"目标武器: {TARGET_WEAPON if TARGET_WEAPON else '未设置（将进入交互模式）'}")
    print(f"显示武器星级: {'是' if SHOW_STAR else '否'}")
    print(f"最低显示星级: {MIN_STAR}星")
    print(f"显示武器类型: {'是' if SHOW_TYPE else '否'}")
    print("=" * 60)

    # 创建分析器实例
    analyzer = WeaponAnalysis(
        excel_file,
        target_weapon=TARGET_WEAPON,
        show_star=SHOW_STAR,
        min_star=MIN_STAR,
        show_type=SHOW_TYPE
    )

    # 直接分析目标武器
    if TARGET_WEAPON:
        analyzer.analyze_weapon(TARGET_WEAPON)
        # print("\n" + "=" * 60)
        # print("分析完成!")
    else:
        # 交互模式
        all_weapons = analyzer.weapons_df['武器名称'].tolist()
        print(f"\n数据库中共有 {len(all_weapons)} 件武器")
        print("输入 'list' 查看所有武器，或输入武器名称开始分析")

        while True:
            print("\n" + "=" * 50)
            user_input = input("请输入武器名称(输入q退出): ").strip()

            if user_input.lower() == 'q':
                break

            if user_input.lower() == 'list':
                print("\n武器列表:")
                for i, weapon in enumerate(all_weapons, 1):
                    weapon_info = analyzer.get_weapon_info(weapon)
                    if weapon_info:
                        star_display = "★" * weapon_info['星级']
                        print(f"{i:3}. {weapon:15} {star_display:6} {weapon_info['类型']}")
                continue

            if user_input not in all_weapons:
                print(f"错误: 武器 '{user_input}' 不存在")
                print("请输入正确的武器名称，或输入 'list' 查看所有武器")
                continue

            # 分析武器
            analyzer.analyze_weapon(user_input)


if __name__ == "__main__":
    main()