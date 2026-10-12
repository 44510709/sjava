# -*- coding: utf-8 -*-
"""
日本品牌代购集中采购系统 · PRD Word 文档生成脚本
设计原则：业务闭环、数据闭环、状态机闭环；技术细节弱化。
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.enum.style import WD_STYLE_TYPE

OUTPUT_PATH = "/Users/wyz/Downloads/sjava/docs/prd/日本品牌代购系统PRD-V1.1.docx"

# ============================================================
# 样式辅助
# ============================================================

def set_cell_bg(cell, color_hex):
    """设置单元格背景色"""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_hex)
    tc_pr.append(shd)


def set_cell_borders(cell):
    """设置单元格边框"""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_borders = OxmlElement('w:tcBorders')
    for border in ['top', 'left', 'bottom', 'right']:
        b = OxmlElement(f'w:{border}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), '4')
        b.set(qn('w:color'), '666666')
        tc_borders.append(b)
    tc_pr.append(tc_borders)


def add_heading_with_style(doc, text, level=1):
    """添加带样式的标题"""
    h = doc.add_heading(text, level=level)
    for run in h.runs:
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        if level == 0:
            run.font.size = Pt(26)
            run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
        elif level == 1:
            run.font.size = Pt(18)
            run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)
        elif level == 2:
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x2C, 0x5F, 0x8C)
        else:
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
    return h


def add_paragraph_text(doc, text, bold=False, size=10.5, color=None, align=None):
    """添加段落"""
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(size)
    run.bold = bold
    if color:
        run.font.color.rgb = color
    return p


def add_bullet(doc, text, level=0):
    """添加项目符号"""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.left_indent = Cm(0.5 + level * 0.5)
    run = p.runs[0] if p.runs else p.add_run(text)
    if not p.runs or p.runs[0].text == '':
        p.add_run(text)
    else:
        p.runs[0].text = text
    for r in p.runs:
        r.font.name = '微软雅黑'
        r._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        r.font.size = Pt(10.5)
    return p


def add_quote_block(doc, text, color_bg='F0F4F8'):
    """添加引用块（浅色背景强调）"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.right_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(10.5)
    run.font.color.rgb = RGBColor(0x33, 0x33, 0x66)
    run.italic = True
    # 背景色
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color_bg)
    pPr.append(shd)
    return p


def add_code_block(doc, text):
    """添加代码/流程图块"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), 'F4F4F4')
    pPr.append(shd)
    return p


def add_data_table(doc, headers, rows, header_bg='1F3A5F', col_widths=None):
    """添加数据表格"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # 设置列宽
    if col_widths:
        for i, width in enumerate(col_widths):
            for cell in table.columns[i].cells:
                cell.width = width

    # 表头
    for i, header in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ''
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(header)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(10.5)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_bg(cell, header_bg)
        set_cell_borders(cell)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # 数据行
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            cell.text = ''
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(str(val))
            run.font.name = '微软雅黑'
            run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
            run.font.size = Pt(10)
            set_cell_borders(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            # 斑马纹
            if r_idx % 2 == 1:
                set_cell_bg(cell, 'F8F9FB')

    return table


def add_page_break(doc):
    doc.add_page_break()


# ============================================================
# 文档主体生成
# ============================================================

def build_document():
    doc = Document()

    # 全局默认字体
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    style.font.size = Pt(10.5)

    # 页面边距
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    # ------------------------------------------------------------
    # 封面
    # ------------------------------------------------------------
    for _ in range(4):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('日  本  品  牌  代  购  集  中  采  购  系  统')
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(28)
    run.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x3A, 0x5F)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('产  品  需  求  文  档 （PRD）')
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(22)
    run.bold = True
    run.font.color.rgb = RGBColor(0x2C, 0x5F, 0x8C)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('系统设计 · 闭环版本 · 扩展增强版')
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    for _ in range(8):
        doc.add_paragraph()

    # 封面元信息表
    cover_table = doc.add_table(rows=6, cols=2)
    cover_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cover_data = [
        ('文档名称', '日本品牌代购集中采购系统 · 产品需求文档（PRD）'),
        ('文档版本', 'V1.1 · 闭环版 · 扩展增强版'),
        ('文档状态', '已定稿 / 待业务方签字确认'),
        ('业务模式', '选品 → 社群引流 → 小程序下单 → 集中采购 → 跨境直邮 → 国内分发'),
        ('文档日期', '2026 年 10 月 12 日'),
        ('密级', '内部使用 · 严禁外传'),
    ]
    for i, (k, v) in enumerate(cover_data):
        c1 = cover_table.rows[i].cells[0]
        c1.text = ''
        p = c1.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(k)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(11)
        run.bold = True
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        set_cell_bg(c1, '1F3A5F')
        set_cell_borders(c1)

        c2 = cover_table.rows[i].cells[1]
        c2.text = ''
        p = c2.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(v)
        run.font.name = '微软雅黑'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        run.font.size = Pt(11)
        set_cell_borders(c2)

    add_page_break(doc)

    # ------------------------------------------------------------
    # 文档说明
    # ------------------------------------------------------------
    add_heading_with_style(doc, '文档说明', level=1)

    add_paragraph_text(doc, '本文档为公司级产品需求文档（PRD），目标是让研发团队在不询问业务方的情况下，能够独立完成系统架构设计、数据库建模与接口开发。')
    add_paragraph_text(doc, '本版本以"业务闭环"为核心设计原则，确保每一个业务场景都能在系统中完整流转，不留断点。', bold=True)

    add_heading_with_style(doc, '核心设计原则', level=2)
    principles = [
        ('订单驱动采购', '没有客户订单，就没有采购行为。系统永远基于订单反推采购需求。'),
        ('后台掌握所有业务与财务规则', '前端展示仅供参考，所有金额、状态、权限校验在后端完成。'),
        ('不信任前端传参', '前端传来的任何数据（价格、折扣、状态）均不直接信任，必须后端重算。'),
        ('不支持用户自助退款', '用户端不出现任何退款入口。退款由后台人员根据采购结果统一处理。'),
        ('系统设计必须闭环', '每一个业务场景都必须有完整的开始、处理、收尾、可追溯链路。'),
        ('模块化边界清晰', '每个模块职责单一，可独立升级、替换或下线，不影响其他模块。'),
        ('业务规则配置化', '服务费率、运费分摊规则、退款规则等业务参数必须配置化管理，不写死在代码中。'),
        ('数据与接口预留扩展', '关键表预留扩展字段，接口支持版本化演进，便于业务变化时平滑升级。'),
    ]
    add_data_table(doc, ['原则', '说明'], principles,
                   col_widths=[Cm(5), Cm(11)])

    add_heading_with_style(doc, '文档结构', level=2)
    structure = [
        ('第 1 章', '产品概述与业务全景'),
        ('第 2 章', '业务闭环设计（核心）'),
        ('第 3 章', '数据闭环设计（核心）'),
        ('第 4 章', '状态机闭环设计（核心）'),
        ('第 5 章', '角色与权限闭环'),
        ('第 6 章', '异常处理闭环'),
        ('第 7 章', '功能模块详细需求'),
        ('第 8 章', '非功能性需求（含扩展性设计）'),
        ('第 9 章', '待业务方确认事项'),
        ('第 10 章', '验收标准（AC）'),
        ('第 11 章', '项目交付清单'),
        ('附录 A', '术语表'),
        ('附录 B', '文档版本管理'),
        ('附录 C', '扩展点清单（V1.1 新增）'),
        ('附录 D', '版本演进路线图（V1.1 新增）'),
    ]
    add_data_table(doc, ['章节', '内容'], structure,
                   col_widths=[Cm(3), Cm(13)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 1 章 产品概述
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 1 章  产品概述', level=1)

    add_heading_with_style(doc, '1.1 产品定位', level=2)
    add_paragraph_text(doc,
        '为日本品牌代购业务提供全链路数字化管理的专用系统，覆盖"商品上架 → 客户下单 → 集中采购 → 跨境物流 → 国内分发 → 售后退款"完整业务闭环。')
    add_paragraph_text(doc,
        '系统由两部分组成：面向消费者的微信小程序，以及面向运营、采购、仓库、财务的 Web 管理后台。')

    add_heading_with_style(doc, '1.2 目标用户', level=2)
    add_data_table(doc, ['角色', '使用端', '核心诉求'],
        [
            ('终端消费者', '微信小程序', '浏览商品、下单付款、查看物流、查看退款结果'),
            ('运营人员', 'Web 后台', '上架商品、审核订单、处理采购异常、发起退款'),
            ('采购人员', 'Web 后台', '生成采购清单、录入采购结果、分配采购数量'),
            ('仓库人员', 'Web 后台', '日本仓收货、发货、录入物流单号'),
            ('财务/管理员', 'Web 后台', '查看报表、导出数据、权限管理'),
        ], col_widths=[Cm(3.5), Cm(3.5), Cm(9)])

    add_heading_with_style(doc, '1.3 业务背景与核心痛点', level=2)
    pains = [
        ('选品上架慢', '后台支持程序化批量录入（Excel 导入、模板复制、批量改价）。'),
        ('采购数量分配乱', '建立采购批次 + 采购分配表，系统自动把实际买到数量分配到具体客户订单。'),
        ('用户退款纠纷', '不支持用户自助退款，所有退款由后台根据采购结果统一处理，状态同步小程序。'),
        ('财务算不清', '报表区分商品款/服务费/运费/国内配送费，消费者支付总额 ≠ 公司收入。'),
        ('跨境物流复杂', '支持多段物流（国际 + 国内）、运费后结算、按规则自动分摊到客户。'),
    ]
    add_data_table(doc, ['业务痛点', '系统解决方案'], pains,
                   col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '1.4 整体业务闭环全景图', level=2)
    add_paragraph_text(doc, '系统全链路业务闭环：从日本官网选品开始，到消费者最终签收（或退款）结束，全程数字化、可追溯。')
    add_code_block(doc,
"""[日本官网选品] → [选品表/商品池]
        ↓
[运营录入后台] ←─程序化批量─→ [小程序商品上架]
        ↓                            ↓
   [商品库]                    [消费者浏览]
                                    ↓
                              [小程序下单/支付]
                                    ↓
                          [订单池：已支付/待采购]
                                    ↓
                          [采购人员生成采购清单]
                                    ↓
                          [去日本官网集中采购]
                                    ↓
                          [采购结果录入（含异常）]
                                    ↓
                          [系统自动分配到客户订单]
                            ↓              ↓
                    [完全成功]         [部分/完全失败]
                            ↓              ↓
                       [日本仓收货]    [采购异常处理]
                            ↓              ↓
                       [国际物流]      [后台发起退款]
                            ↓              ↓
                       [国内分发]      [小程序同步状态]
                            ↓              ↓
                          [签收]        [已退款]
                            ↓              ↓
                          [完成] ←────────┘
                          （全链路闭环结束）""")

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 2 章 业务闭环设计（核心）
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 2 章  业务闭环设计', level=1)
    add_quote_block(doc,
        '本章是本文档核心。系统必须确保每一个业务场景都有完整的开始、处理、收尾、可追溯链路，形成业务闭环。任何断点都会导致数据不一致或业务纠纷。')

    # 2.1 商品生命周期闭环
    add_heading_with_style(doc, '2.1 商品生命周期闭环', level=2)
    add_code_block(doc,
"""[选品发现] → [选品表登记] → [运营录入后台] → [SKU 配置+定价] → [上架/小程序可售]
                                                                      ↓
                                                              [消费者下单]
                                                                      ↓
                                                          [产生历史订单]
                                                                      ↓
                                                           [禁止物理删除]
                                                                      ↓
                                                          [仅可下架/停售]
                                                                      ↓
                                                          [商品归档/不再上新]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '起点：日本官网选品 / 运营发现')
    add_bullet(doc, '终点：商品归档下架，不再产生新订单')
    add_bullet(doc, '保护机制：只要有历史订单，商品/SKU 就只能下架，不能删除')
    add_bullet(doc, '价格变更：每次改价记录价格历史（before/after/操作人/时间）')

    # 2.2 订单生命周期闭环
    add_heading_with_style(doc, '2.2 订单生命周期闭环', level=2)
    add_code_block(doc,
"""[待支付] → 支付成功 → [已支付/待采购]
                              ↓
                ┌─────────────┴─────────────┐
                ↓                            ↓
        [全部采购成功]              [部分采购失败]
                ↓                            ↓
        [已采购/待发货]            [采购异常/部分退款]
                ↓                            ↓
        [已发国际物流]            [完全采购失败]
                ↓                            ↓
        [国际运输中]              [已退款/已关闭]
                ↓
        [已发国内物流]
                ↓
        [国内配送中]
                ↓
        [已签收] → [已完成] → [订单归档]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '起点：用户在小程序提交订单')
    add_bullet(doc, '终点：订单归档（已完成 / 已关闭）')
    add_bullet(doc, '金额快照：下单时所有价格、地址、服务费全部快照写入订单明细')
    add_bullet(doc, '状态联动：订单状态变更会触发小程序通知、物流同步、财务记账')

    # 2.3 采购生命周期闭环
    add_heading_with_style(doc, '2.3 采购生命周期闭环（核心难点）', level=2)
    add_paragraph_text(doc,
        '采购闭环是整个系统最复杂的部分。难点在于：客户订单分散，但采购是集中行为（一次采购可能涉及多个客户订单），如何把实际买到的商品"精准分配"回每个客户的订单上。')

    add_code_block(doc,
"""[已支付/待采购订单池]
        ↓ (按 SKU 聚合)
[待采购清单]
        ↓ (采购人员去日本官网采购)
[采购批次：采购中]
        ↓ (录入实际采购结果)
[采购批次：部分完成/已完成]
        ↓ (系统自动分配)
[采购分配表 purchase_allocation]
        ↓
   ┌────┴────┐
   ↓         ↓
[完全满足] [部分/全部缺货]
   ↓         ↓
[待发货] [采购异常]
              ↓
       [后台发起退款] → [订单状态更新] → [小程序同步]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '起点：已支付订单进入"待采购"状态')
    add_bullet(doc, '终点：所有商品要么发货到客户，要么发起退款')
    add_bullet(doc, '核心数据：purchase_allocation（采购分配表）记录每一件商品的去向')
    add_bullet(doc, '异常兜底：任何分配不出去的商品，自动进入采购异常表，等待运营处理')

    # 2.4 退款生命周期闭环
    add_heading_with_style(doc, '2.4 退款生命周期闭环（后台单向）', level=2)
    add_quote_block(doc,
        '用户端不存在任何退款入口。所有退款均由后台人员（运营/财务/管理员）根据采购异常或售后需求发起。')

    add_code_block(doc,
"""[采购异常/售后请求]
        ↓ (运营识别)
[后台人员发起退款]
        ↓ (选择订单+退款金额)
[系统后端计算退款金额]
        ↓ (按件数比例计算商品+服务费)
[校验可退余额]
        ↓
[调用微信退款 API]
        ↓
[退款结果回调]
        ↓
   ┌────┴────┐
   ↓         ↓
[退款成功] [退款失败]
   ↓         ↓
[更新订单状态]  [保留状态,支持重试]
   ↓
[小程序订阅消息通知]
   ↓
[用户端看到退款结果]
   ↓
[订单标记为已退款/部分退款]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '起点：后台人员识别到需要退款的场景（采购异常或售后）')
    add_bullet(doc, '终点：用户在小程序看到退款结果')
    add_bullet(doc, '金额后端计算：禁止前端传金额，禁止运营手动输入金额')
    add_bullet(doc, '幂等保障：同一笔退款不能重复发起，不能重复成功')

    # 2.5 物流生命周期闭环
    add_heading_with_style(doc, '2.5 物流生命周期闭环', level=2)
    add_code_block(doc,
"""[采购批次完成]
        ↓
[日本仓收货核验]
        ↓ (应收 vs 实收,记录破损/少件)
[国际物流单号录入]
        ↓ (EMS / SF 国际等)
[国际运输中]
        ↓
[到达国内仓]
        ↓ (按客户/订单拆分包裹)
[国内快递单号录入]
        ↓ (顺丰/中通/京东等)
[国内运输中]
        ↓
[签收确认]
        ↓
[订单状态:已完成]
        ↓
[触发小程序通知 + 财务结算运费]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '起点：采购批次完成，日本仓收货')
    add_bullet(doc, '终点：用户签收，订单关闭')
    add_bullet(doc, '多段物流：国际段 + 国内段分开管理，支持一个订单多个包裹')
    add_bullet(doc, '运费后结算：国际运费到仓后按规则分摊到客户订单')

    # 2.6 财务数据闭环
    add_heading_with_style(doc, '2.6 财务数据闭环', level=2)
    add_code_block(doc,
"""[消费者支付总额]
        ↓
   ┌────┴────┬──────────┬──────────┐
   ↓         ↓          ↓          ↓
[商品采购款] [服务费] [国际运费] [国内配送费]
   ↓         ↓          ↓          ↓
[成本]    [毛利]    [代收代付]  [成本]
   ↓         ↓          ↓          ↓
[支付供应商] [公司收入] [支付物流] [支付快递]
              ↑
          (真正的公司收入)

[退款闭环反向]
[商品退款] [服务费退款] [运费退款] [国内快递退款]
   ↓         ↓          ↓          ↓
[扣减成本] [扣减毛利] [扣减代收] [扣减成本]""")

    add_paragraph_text(doc, '闭环要点：', bold=True)
    add_bullet(doc, '消费者支付总额 ≠ 公司收入')
    add_bullet(doc, '服务费才是真正的毛利')
    add_bullet(doc, '运费、国内配送费是代收代付，不算利润')
    add_bullet(doc, '退款必须从对应科目扣减，保持账目平衡')

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 3 章 数据闭环设计（核心）
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 3 章  数据闭环设计', level=1)
    add_quote_block(doc,
        '本章定义系统核心数据实体及其相互关系。目标是确保任何一个业务事件，都能追溯到完整的链路上下游。')

    # 3.1 核心实体清单
    add_heading_with_style(doc, '3.1 核心数据实体清单', level=2)
    entities = [
        ('系统层', 'sys_user / sys_role / sys_permission', '后台账号、角色、权限'),
        ('商品层', 'product / product_sku / product_price_history', '商品 SPU、SKU、价格历史'),
        ('订单层', 'orders / order_item / order_logistics_relation', '订单主表、明细、物流关联'),
        ('支付层', 'payment_order / refund_order', '支付流水、退款流水'),
        ('采购层', 'purchase_batch / purchase_batch_item / purchase_allocation / purchase_exception',
         '采购批次、批次明细、分配关系、异常处理'),
        ('物流层', 'warehouse_receipt / logistics_order / package', '收货记录、物流单、包裹'),
        ('用户层', 'customer / customer_address', '消费者档案、收货地址'),
        ('日志层', 'operation_log', '操作日志（防删改）'),
    ]
    add_data_table(doc, ['层级', '核心表名', '作用'], entities,
                   col_widths=[Cm(3), Cm(7), Cm(6)])

    # 3.2 数据流转闭环图
    add_heading_with_style(doc, '3.2 数据流转闭环图', level=2)
    add_code_block(doc,
"""        ┌──────────┐
        │  customer│
        └────┬─────┘
             ↓ (下单)
        ┌──────────┐
        │  orders  │←──┐
        └────┬─────┘   │
             ↓         │
      ┌────────────┐   │
      │ order_item │   │
      └────┬───────┘   │
           ↓           │
    ┌──────────────┐    │
    │product_sku   │←───┤ (商品参考)
    └──────────────┘    │
                       │
   ┌──────────────┐     │
   │purchase_batch├─────┘ (按订单聚合)
   └──────┬───────┘
          ↓
 ┌──────────────────┐
 │purchase_batch_item│
 └────────┬──────────┘
          ↓ (录入)
 ┌──────────────────────┐
 │ purchase_allocation  │ ← 灵魂表
 └────────┬─────────────┘
          ↓ (分配)
 ┌──────────────┐
 │  order_item  │ (更新已采购数量)
 └──────┬───────┘
        ↓
 ┌──────────────┐
 │   package    │ (按订单/客户打包)
 └──────┬───────┘
        ↓
 ┌──────────────────┐
 │logistics_order   │
 └──────┬───────────┘
        ↓
 ┌─────────────────┐
 │order_logistics  │
 │   _relation     │
 └──────┬──────────┘
        ↓
   [签收完成]

   异常分支:
   purchase_exception → refund_order → orders(状态更新)""")

    # 3.3 关键链路追溯
    add_heading_with_style(doc, '3.3 关键链路追溯（核心闭环验证）', level=2)
    add_paragraph_text(doc,
        '系统必须支持以下五条追溯链路。这是验证数据闭环是否成立的核心标准。')

    add_heading_with_style(doc, '链路 1：订单 → 采购 → 物流 → 签收', level=3)
    add_code_block(doc,
"""输入：订单号 = ORD20261012001
追溯路径：
  orders → order_item
       → purchase_allocation (根据 order_item_id 反查)
       → purchase_batch_item
       → purchase_batch (批次详情)
       → logistics_order (国际物流)
       → package → order_logistics_relation
       → 包裹签收记录
输出：完整的"从订单到客户签收"全链路时间轴""")

    add_heading_with_style(doc, '链路 2：用户 → 订单 → 退款', level=3)
    add_code_block(doc,
"""输入：用户 ID = 10086
追溯路径：
  customer → orders (该用户所有订单)
          → order_item (订单明细)
          → refund_order (如有退款)
输出：用户的消费历史、退款历史、消费总额""")

    add_heading_with_style(doc, '链路 3：商品 → SKU → 订单明细', level=3)
    add_code_block(doc,
"""输入：商品 ID = P00001
追溯路径：
  product → product_sku
         → order_item (历史订单引用)
         → orders (订单主表)
输出：该商品的所有历史订单、销售统计、退货率""")

    add_heading_with_style(doc, '链路 4：采购批次 → 分配 → 订单', level=3)
    add_code_block(doc,
"""输入：批次号 = PB20261012-001
追溯路径：
  purchase_batch → purchase_batch_item
                → purchase_allocation
                → order_item (具体订单明细)
                → orders → customer
输出：该批次的所有客户、对应订单、收货人""")

    add_heading_with_style(doc, '链路 5：异常 → 退款 → 订单状态', level=3)
    add_code_block(doc,
"""输入：异常 ID = EX20261012-001
追溯路径：
  purchase_exception → purchase_batch_item
                    → purchase_allocation
                    → order_item
                    → refund_order
                    → orders (状态更新记录)
输出：异常发生 → 退款处理 → 订单最终状态的完整时间轴""")

    # 3.4 数据一致性保障
    add_heading_with_style(doc, '3.4 数据一致性保障闭环', level=2)
    add_paragraph_text(doc, '系统必须在以下场景中保证数据一致性：', bold=True)

    consistency = [
        ('创建订单', '订单主表 + 明细表 + 价格快照必须在同一事务内写入', 'P0'),
        ('采购分配', '采购分配表 + 订单明细更新 + 异常表更新必须在同一事务内', 'P0'),
        ('发起退款', '退款单 + 订单状态 + 微信退款调用必须保证一致', 'P0'),
        ('物流更新', '物流单 + 订单关联 + 包裹状态必须联动更新', 'P0'),
        ('价格变更', '商品改价记录 + 历史订单快照不受影响', 'P0'),
        ('金额计算', '所有金额使用 DECIMAL 精度，禁止浮点', 'P0'),
        ('幂等处理', '微信回调重复推送、退款重试不能产生副作用', 'P0'),
    ]
    add_data_table(doc, ['场景', '一致性要求', '优先级'], consistency,
                   col_widths=[Cm(3.5), Cm(11), Cm(1.5)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 4 章 状态机闭环设计（核心）
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 4 章  状态机闭环设计', level=1)
    add_quote_block(doc,
        '系统的每一个核心实体都有自己的状态机。状态机之间存在联动关系：一个状态的变化会触发另一个状态的变化。设计良好的状态机，是业务闭环不出现断点的根本保障。')

    # 4.1 订单状态机
    add_heading_with_style(doc, '4.1 订单状态机', level=2)
    order_states = [
        ('PENDING_PAY', '待支付', '用户提交订单，未支付', '支付成功 / 超时取消'),
        ('PAID_PURCHASE', '已支付/待采购', '支付成功，等待采购', '采购完成 / 部分采购失败'),
        ('PURCHASED', '已采购/待发货', '采购完成，等待发货', '发出国际物流'),
        ('INTERNATIONAL', '国际运输中', '国际段物流在途', '到达国内仓'),
        ('DOMESTIC', '国内配送中', '国内段快递在途', '用户签收'),
        ('COMPLETED', '已完成', '用户签收，订单关闭', '订单归档'),
        ('REFUNDING', '退款中', '部分退款处理中', '退款完成 / 退款失败'),
        ('PARTIAL_REFUNDED', '部分退款', '已部分退款,订单继续', '继续发货 / 继续退款'),
        ('REFUNDED', '已退款', '全额退款,订单关闭', '订单归档'),
        ('CLOSED', '已关闭', '超时未支付或主动取消', '订单归档'),
    ]
    add_data_table(doc, ['状态码', '状态名', '含义', '下一状态'],
                   order_states,
                   col_widths=[Cm(3), Cm(3), Cm(4), Cm(6)])

    # 4.2 采购批次状态机
    add_heading_with_style(doc, '4.2 采购批次状态机', level=2)
    purchase_states = [
        ('DRAFT', '草稿', '采购人员创建批次,未提交', '提交'),
        ('PENDING', '待采购', '批次已生成,等待采购', '开始采购'),
        ('IN_PROGRESS', '采购中', '已下单日本官网', '录入结果'),
        ('PARTIAL', '部分完成', '部分 SKU 已买到', '继续录入 / 关闭'),
        ('COMPLETED', '已完成', '全部 SKU 采购完成', '订单归档'),
        ('CANCELLED', '已取消', '批次取消', '订单归档'),
    ]
    add_data_table(doc, ['状态码', '状态名', '含义', '下一状态'],
                   purchase_states,
                   col_widths=[Cm(3), Cm(3), Cm(6), Cm(4)])

    # 4.3 退款状态机
    add_heading_with_style(doc, '4.3 退款状态机', level=2)
    refund_states = [
        ('PENDING', '待审核', '后台发起退款,等待财务审核', '审核通过'),
        ('APPROVED', '已审核', '审核通过,准备调用微信退款', '调用微信退款'),
        ('REFUNDING', '退款中', '微信退款处理中', '退款成功 / 退款失败'),
        ('SUCCESS', '退款成功', '资金已退给用户', '订单状态更新'),
        ('FAILED', '退款失败', '微信退款失败,需重试', '重试 / 人工处理'),
    ]
    add_data_table(doc, ['状态码', '状态名', '含义', '下一状态'],
                   refund_states,
                   col_widths=[Cm(3), Cm(3), Cm(6), Cm(4)])

    # 4.4 物流状态机
    add_heading_with_style(doc, '4.4 物流状态机', level=2)
    logistics_states = [
        ('CREATED', '已创建', '包裹已打包,等待发出', '已发出'),
        ('SHIPPED', '已发出', '已交付物流公司', '运输中'),
        ('IN_TRANSIT', '运输中', '物流运输中', '到达目的仓 / 派送中'),
        ('DELIVERING', '派送中', '快递员派送', '签收 / 派送失败'),
        ('DELIVERED', '已签收', '用户签收', '订单完成'),
        ('EXCEPTION', '异常', '丢件/破损/无法派送', '售后处理'),
    ]
    add_data_table(doc, ['状态码', '状态名', '含义', '下一状态'],
                   logistics_states,
                   col_widths=[Cm(3), Cm(3), Cm(6), Cm(4)])

    # 4.5 状态联动
    add_heading_with_style(doc, '4.5 状态联动关系（核心）', level=2)
    add_paragraph_text(doc,
        '系统的状态机不是独立的，而是相互联动。任何一个状态的变化都可能触发其他状态的变化。')
    add_code_block(doc,
"""订单状态变化        触发
─────────────      ─────────────────────
待支付 → 已支付    →  通知采购池新增
                   →  推送支付成功消息
                   →  财务记账

已支付 → 部分退款  →  生成采购异常
                   →  触发退款流程

全部采购完成       →  采购批次进入"已完成"
                   →  通知仓库准备发货
                   →  生成包裹

发货 → 国际运输    →  同步小程序物流状态
                   →  推送发货通知

国内签收           →  订单标记为"已完成"
                   →  推送签收通知
                   →  触发评价/复购引导

退款成功           →  订单标记为"已退款"
                   →  推送退款通知
                   →  财务账目扣减""")

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 5 章 角色与权限闭环
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 5 章  角色与权限闭环', level=1)

    add_heading_with_style(doc, '5.1 角色定义', level=2)
    roles = [
        ('超级管理员', '全部权限，包括账号管理、权限分配'),
        ('运营', '商品上下架、订单查询、退款发起（需财务审核）'),
        ('采购', '采购批次管理、采购结果录入、采购分配'),
        ('仓库', '收货记录、物流录入、包裹管理'),
        ('财务', '退款审核、报表查看、导出数据'),
        ('只读账号', '仅查询,无任何修改权限'),
    ]
    add_data_table(doc, ['角色', '核心权限'], roles,
                   col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '5.2 权限闭环规则', level=2)
    add_bullet(doc, '基于角色的权限控制（RBAC）')
    add_bullet(doc, '防止水平越权：用户只能查看权限范围内的订单')
    add_bullet(doc, '敏感字段按权限脱敏（手机号、地址）')
    add_bullet(doc, '关键操作（改价、退款、导出、删除）必须留操作日志')
    add_bullet(doc, '权限变更必须审计，记录操作人、时间、内容')

    add_heading_with_style(doc, '5.3 操作审计闭环', level=2)
    add_paragraph_text(doc,
        '所有关键操作必须记录操作日志，形成审计闭环。日志一旦写入不可修改、不可删除。')
    audit_items = [
        ('登录/登出', '每次登录登出记录'),
        ('商品改价', '记录 before/after/操作人/时间'),
        ('退款操作', '记录发起人、金额、原因'),
        ('采购分配', '记录分配数量、对应订单'),
        ('物流更新', '记录单号、状态变更'),
        ('权限变更', '记录变更前后权限'),
        ('数据导出', '记录导出范围、操作人'),
    ]
    add_data_table(doc, ['操作类型', '审计内容'], audit_items,
                   col_widths=[Cm(4), Cm(12)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 6 章 异常处理闭环
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 6 章  异常处理闭环', level=1)
    add_quote_block(doc,
        '业务异常不可怕，可怕的是异常发生后系统没有兜底机制。本章定义所有已知异常的分类与处理闭环。')

    add_heading_with_style(doc, '6.1 业务异常分类', level=2)
    exceptions = [
        ('采购异常', '缺货、限购、涨价、停产、官网改版', 'purchase_exception 表 + 触发退款'),
        ('支付异常', '支付超时、支付失败、重复回调', '订单状态保持 + 重试机制'),
        ('退款异常', '微信退款失败、金额超限', '状态保留 + 重试 / 人工处理'),
        ('物流异常', '丢件、破损、无法派送、清关问题', '售后工单 + 补发 / 退款'),
        ('系统异常', '接口超时、数据库异常、第三方故障', '日志告警 + 人工介入'),
        ('合规异常', '商品违规、价格异常、用户投诉', '运营介入 + 商品下架'),
    ]
    add_data_table(doc, ['异常类型', '具体场景', '处理闭环'], exceptions,
                   col_widths=[Cm(3), Cm(6), Cm(7)])

    add_heading_with_style(doc, '6.2 异常升级机制', level=2)
    add_code_block(doc,
"""[一级异常：自动处理]
  采购异常 → 系统自动触发退款流程
  支付回调重复 → 幂等拦截
  ↓ 升级条件:处理失败/超时
[二级异常：人工处理]
  退款失败 → 财务人员重试
  物流异常 → 仓库/客服处理
  ↓ 升级条件:超过 24h 未解决
[三级异常：管理介入]
  严重异常 → 通知管理员
  批量异常 → 启动应急流程""")

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 7 章 功能模块详细需求
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 7 章  功能模块详细需求', level=1)

    # 7.1 商品与SKU管理
    add_heading_with_style(doc, '7.1 商品与 SKU 管理模块', level=2)
    add_paragraph_text(doc, '采用 SPU + SKU 双层模型。SPU 定义"是什么商品"，SKU 定义"具体规格"。')

    add_heading_with_style(doc, '商品字段', level=3)
    add_data_table(doc, ['字段', '说明'],
        [
            ('商品 ID', '唯一标识'),
            ('商品名称', '中文商品名'),
            ('品牌', '品牌名'),
            ('分类', '一级分类'),
            ('官网链接', '日本官网商品页 URL'),
            ('主图 / 详情图', '小程序展示用'),
            ('状态', '草稿 / 上架 / 下架'),
        ], col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, 'SKU 字段', level=3)
    add_data_table(doc, ['字段', '说明'],
        [
            ('SKU ID', '唯一标识'),
            ('规格组合', '如"黑色/27cm"'),
            ('官网规格标识', '官网该规格的唯一标识'),
            ('当前售价', '小程序显示价'),
            ('服务费', '代购服务费'),
            ('状态', '可下单 / 停售'),
        ], col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '程序化批量录入（核心需求）', level=3)
    add_paragraph_text(doc, '商品上架是高频操作，必须支持程序化批量录入，简化运营工作量。')
    add_data_table(doc, ['录入方式', '说明', '适用场景'],
        [
            ('Excel 批量导入', '下载模板 → 填写 → 上传', '一次性上架几十上百款'),
            ('复制粘贴官网商品', '粘贴官网 URL → 系统解析', '快速上架单款'),
            ('模板复制', '复制已上架商品 → 改字段', '上架同款不同规格'),
            ('批量改价', '选中多个 SKU → 统一调价', '调价场景'),
        ], col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, '商品业务规则', level=3)
    add_bullet(doc, '已产生订单的商品 / SKU 不能物理删除，只能下架或停售')
    add_bullet(doc, '下单时后端必须重算 SKU 最新价格')
    add_bullet(doc, '价格变更必须记录 before / after / 操作人 / 时间')
    add_bullet(doc, '无实体库存，允许超卖，最终以日本官网实际采购为准')

    # 7.2 订单与支付
    add_heading_with_style(doc, '7.2 订单与支付模块', level=2)
    add_heading_with_style(doc, '订单主表字段', level=3)
    add_data_table(doc, ['字段', '说明'],
        [
            ('订单号', '业务唯一编号'),
            ('用户 ID', '关联消费者'),
            ('商品总金额', '所有 SKU 售价合计'),
            ('服务费总额', '所有 SKU 服务费合计'),
            ('国际运费分摊', '后结算后写入'),
            ('国内快递费', '通常包邮'),
            ('应付金额', '后端计算结果'),
            ('已付金额', '实际支付金额'),
            ('已退款金额', '累计已退'),
            ('订单状态', '见状态机章节'),
            ('收货地址快照', '下单时地址完整快照'),
            ('下单/支付/完成时间', '关键时间戳'),
        ], col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '订单核心规则', level=3)
    add_bullet(doc, '价格后端重算：前端传 1 元也无效，后端按 SKU 最新价 + 服务费重算')
    add_bullet(doc, '事务一致性：订单主表和明细表必须同事务写入')
    add_bullet(doc, '支付幂等：微信支付回调校验签名 + 订单号幂等')
    add_bullet(doc, '订单快照：下单时所有价格、规格、地址必须快照写入明细')

    # 7.3 采购与分配
    add_heading_with_style(doc, '7.3 集中采购与分配模块（核心难点）', level=2)

    add_heading_with_style(doc, '采购清单生成', level=3)
    add_paragraph_text(doc,
        '采购人员进入采购模块，系统自动按 SKU 聚合所有"已支付且未采购"的订单明细，生成待采购清单。清单支持导出 Excel，方便采购人员带去日本官网。')

    add_heading_with_style(doc, '采购批次管理', level=3)
    add_data_table(doc, ['字段', '说明'],
        [
            ('批次号', '业务唯一编号'),
            ('渠道', '日本官网 / Amazon JP / 线下'),
            ('状态', '待采购 / 采购中 / 部分完成 / 已完成 / 已取消'),
            ('采购总成本', '商品采购款'),
            ('国际运费', '后结算'),
            ('创建人 / 时间', '审计字段'),
        ], col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '采购结果录入与分配（核心）', level=3)
    add_quote_block(doc,
        '采购分配表 purchase_allocation 是整个系统的灵魂表。记录每一件实际采购到的商品，对应分配到哪个客户的哪笔订单明细。')

    add_paragraph_text(doc, '典型场景：')
    add_code_block(doc,
"""批次需求：SKU-X 共 10 件
  客户 A：3 件
  客户 B：5 件
  客户 C：2 件

实际采购：8 件（缺货 2 件）

系统自动分配（先到先得 / 按提交时间优先）：
  客户 A：3 件 ✓
  客户 B：4 件（部分满足）
  客户 C：1 件（部分满足）

剩余 2 件（未分配）：
  → 进入采购异常表
  → 系统提示运营发起对应客户的退款""")

    add_bullet(doc, '采购结果录入必须防重：同一批次同一 SKU 不能重复分配')
    add_bullet(doc, '分配逻辑由系统执行，运营人员不能手动指定（避免主观偏差）')

    # 7.4 退款
    add_heading_with_style(doc, '7.4 退款模块', level=2)
    add_quote_block(doc,
        '用户端不允许出现任何退款入口。所有退款由后台人员发起。')

    add_heading_with_style(doc, '退款计算规则', level=3)
    add_data_table(doc, ['项目', '退款规则'],
        [
            ('商品金额', '按件数比例退'),
            ('服务费', '按件数比例退（与商品同步）'),
            ('国际运费', '仅在该订单完全未发国际物流时退'),
            ('国内快递', '未发货全退，已发货按公司政策'),
            ('总额校验', '累计退款金额 ≤ 已付金额'),
        ], col_widths=[Cm(4), Cm(12)])

    add_bullet(doc, '退款金额由后端计算，禁止前端传金额')
    add_bullet(doc, '部分退款不能将整个订单标记为全额退款')
    add_bullet(doc, '退款失败需保留状态，支持重试')
    add_bullet(doc, '退款完成后自动推送小程序订阅消息')

    # 7.5 仓储物流
    add_heading_with_style(doc, '7.5 仓储与物流模块', level=2)
    add_bullet(doc, '日本仓收货：记录应收 / 实收 / 破损 / 少件，差异自动进入异常')
    add_bullet(doc, '国际物流：录入国际运单号，跟踪到国内仓')
    add_bullet(doc, '国内物流：按客户/订单拆分包裹，录入国内快递单号')
    add_bullet(doc, '运费分摊：国际运费后结算，按业务规则分摊到客户订单')
    add_bullet(doc, '物流状态同步：物流更新后自动同步小程序')

    # 7.6 财务与报表
    add_heading_with_style(doc, '7.6 财务与报表模块', level=2)
    add_quote_block(doc,
        '消费者支付总额 ≠ 公司收入。报表必须区分商品采购款 / 服务费 / 运费 / 国内配送费。')

    add_heading_with_style(doc, '报表维度', level=3)
    add_data_table(doc, ['维度', '报表内容'],
        [
            ('订单维度', '订单列表、详情、收支明细'),
            ('用户维度', '消费排行、消费历史、地址簿'),
            ('商品维度', '销售排行、SKU 明细、退款率'),
            ('财务维度', '营收汇总、退款汇总、毛利统计、资金流监控'),
        ], col_widths=[Cm(4), Cm(12)])

    add_heading_with_style(doc, '报表要求', level=3)
    add_bullet(doc, '所有报表支持导出 Excel')
    add_bullet(doc, '大数据量导出使用异步任务，完成后通知下载')
    add_bullet(doc, '所有列表强制分页，禁止一次性加载全量')

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 8 章 非功能性需求
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 8 章  非功能性需求', level=1)

    add_heading_with_style(doc, '8.1 数据一致性', level=2)
    add_bullet(doc, '关键操作必须在数据库事务内完成（创建订单、采购分配、退款处理、物流更新）')
    add_bullet(doc, '外部回调必须幂等（微信支付回调、退款回调）')
    add_bullet(doc, '所有金额字段使用 DECIMAL(12,2)，严禁 Float/Double')
    add_bullet(doc, '关键字段加乐观锁，防并发覆盖')

    add_heading_with_style(doc, '8.2 安全与权限', level=2)
    add_bullet(doc, '所有后台 API 必须校验角色 + 数据权限')
    add_bullet(doc, '敏感字段（手机号、地址）按权限脱敏')
    add_bullet(doc, '关键操作记录操作日志（防删改）')
    add_bullet(doc, '微信支付密钥、数据库密码从环境变量读取，不写在代码里')
    add_bullet(doc, '所有金额、状态、权限校验必须在后端做')

    add_heading_with_style(doc, '8.3 性能要求', level=2)
    perf = [
        ('商品列表', 'p99 < 500ms'),
        ('订单列表', 'p99 < 800ms'),
        ('提交订单', 'p99 < 1s'),
        ('后台首页加载', 'p99 < 1s'),
        ('报表导出', '异步执行,不阻塞主流程'),
    ]
    add_data_table(doc, ['接口', '性能要求'], perf,
                   col_widths=[Cm(6), Cm(10)])

    add_heading_with_style(doc, '8.4 可观测性', level=2)
    add_bullet(doc, '所有 API 记录请求 / 响应日志（脱敏后）')
    add_bullet(doc, '关键链路支持按订单号 / 批次号追踪')
    add_bullet(doc, '业务异常埋点（退款失败、采购异常、回调失败）')
    add_bullet(doc, '慢 SQL 监控（> 500ms 自动告警）')

    # 8.5 扩展性设计（V1.1 新增）
    add_heading_with_style(doc, '8.5 扩展性设计（迭代扩展保障）', level=2)
    add_quote_block(doc,
        '业务会变、规模会涨、规则会调。系统设计必须为变化预留空间，而不是每次业务调整都要重写代码。本节定义系统的扩展性保障机制。')

    add_heading_with_style(doc, '8.5.1 模块化边界', level=3)
    add_paragraph_text(doc, '系统按职责拆分为 7 个核心模块，每个模块独立部署、独立升级，模块间通过明确的接口契约交互：')
    add_data_table(doc, ['模块', '职责', '可替换性'],
        [
            ('商品中心', '商品 / SKU 管理、上下架、价格维护', '可替换为外部 ERP 或 PIM 系统'),
            ('订单中心', '订单创建、状态流转、退款联动', '核心模块，业务稳定后不建议替换'),
            ('采购中心', '采购批次、分配逻辑、异常处理', '可独立升级采购规则'),
            ('物流中心', '包裹、物流单号、轨迹跟踪', '可对接第三方物流 API'),
            ('支付中心', '支付、退款、流水管理', '可扩展支持支付宝、银联等多渠道'),
            ('财务中心', '营收、退款、毛利、资金流统计', '可对接外部财务系统'),
            ('通知中心', '小程序订阅消息、短信、邮件', '可扩展支持多渠道触达'),
        ], col_widths=[Cm(3), Cm(7), Cm(6)])

    add_paragraph_text(doc, '模块化收益：', bold=True)
    add_bullet(doc, '业务变更时只影响单个模块，不波及其他模块')
    add_bullet(doc, '每个模块可独立测试、独立部署')
    add_bullet(doc, '团队按模块划分职责，提升协作效率')
    add_bullet(doc, '外部系统对接只发生在边界模块（如商品中心对接 PIM）')

    add_heading_with_style(doc, '8.5.2 配置化 vs 硬编码', level=3)
    add_paragraph_text(doc,
        '业务规则优先配置化，避免每次业务调整都修改代码并发布。')
    add_data_table(doc, ['项目', '处理方式', '理由'],
        [
            ('服务费率', '配置中心', '不同品类服务费不同,需灵活调整'),
            ('运费分摊规则', '配置 + 策略模式', '业务可能调整分摊逻辑'),
            ('退款规则', '配置化规则引擎', '业务规则经常微调'),
            ('采购分配规则', '策略模式 + 配置', '可切换"先到先得"或"按金额优先"'),
            ('状态机流转条件', '状态机配置', '业务状态可能新增'),
            ('金额计算公式', '配置 + 公式引擎', '避免改代码'),
            ('通知触发条件', '配置化', '运营策略经常变'),
        ], col_widths=[Cm(3.5), Cm(4.5), Cm(8)])

    add_paragraph_text(doc, '配置化管理工具建议：', bold=True)
    add_bullet(doc, '轻量方案：Nacos / Apollo 配置中心')
    add_bullet(doc, '可视化方案：自建配置管理后台（运营可自助修改）')
    add_bullet(doc, '规则引擎方案：Aviator / Easy Rules（复杂规则场景）')

    add_heading_with_style(doc, '8.5.3 数据扩展字段预留', level=3)
    add_paragraph_text(doc,
        '关键表预留扩展字段，避免业务变化时频繁 ALTER TABLE。')
    add_data_table(doc, ['表名', '预留扩展字段', '用途'],
        [
            ('orders', 'ext_field_1 ~ ext_field_10', '订单级自定义属性（业务标签等）'),
            ('order_item', 'ext_field_1 ~ ext_field_5', '明细级自定义属性'),
            ('product', 'metadata JSON', '商品元数据（结构化扩展）'),
            ('product_sku', 'spec_extra JSON', '规格扩展属性'),
            ('customer', 'tags VARCHAR(500)', '用户标签体系'),
            ('customer', 'level VARCHAR(20)', '用户等级（VIP 等）'),
            ('purchase_batch', 'extra_info JSON', '批次自定义信息'),
            ('logistics_order', 'ext_data JSON', '物流扩展字段'),
        ], col_widths=[Cm(3.5), Cm(5), Cm(7.5)])

    add_paragraph_text(doc, '扩展字段使用规范：', bold=True)
    add_bullet(doc, '通用字段用 ext_field_N，结构化数据用 JSON 字段')
    add_bullet(doc, '扩展字段必须有业务含义说明文档')
    add_bullet(doc, '扩展字段变更要记录到产品需求版本')

    add_heading_with_style(doc, '8.5.4 接口版本化管理', level=3)
    add_paragraph_text(doc, '所有对外接口必须支持版本化演进，避免一次升级导致所有客户端崩溃。')
    add_code_block(doc,
"""接口版本规则：
  - URL 必须包含版本号：/api/v1/order/create
  - 同一接口至少向后兼容 2 个版本
  - 废弃 API 必须提前 3 个月公告
  - 版本切换通过网关路由，不改业务代码

示例：
  V1.0：/api/v1/order/create  (基础下单)
  V1.1：/api/v1/order/create  (新增备注字段,可选)
  V1.5：/api/v2/order/create  (重构入参结构,V1 仍可用)
  V2.0：/api/v2/order/create  (V1 标记 deprecated)
  V2.5：/api/v3/order/create  (V1 下线)""")

    add_heading_with_style(doc, '8.5.5 通知与渠道扩展', level=3)
    add_paragraph_text(doc, '通知中心设计为"渠道无关"，便于未来扩展通知渠道：')
    channels = [
        ('小程序订阅消息', '已支持', '用户触达主渠道'),
        ('短信通知', '预留扩展', '重要节点（支付、退款）'),
        ('邮件通知', '预留扩展', '财务对账、订单详情'),
        ('微信公众号模板消息', '预留扩展', '辅助触达'),
        ('Webhook', '预留扩展', '对接企业内部系统'),
    ]
    add_data_table(doc, ['渠道', '当前状态', '适用场景'], channels,
                   col_widths=[Cm(4.5), Cm(3.5), Cm(8)])

    add_heading_with_style(doc, '8.5.6 多端扩展能力', level=3)
    add_paragraph_text(doc, '业务可能扩展到多端（小程序、H5、APP、第三方平台）。系统设计必须支持：')
    add_bullet(doc, '后端 API 不绑定任何客户端')
    add_bullet(doc, '用户体系统一（一个用户可在多端登录）')
    add_bullet(doc, '订单 / 商品数据多端共享')
    add_bullet(doc, '权限按端独立配置（如 H5 只读、APP 可下单）')

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 9 章 待业务方确认事项
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 9 章  待业务方确认事项', level=1)
    add_quote_block(doc,
        '以下规则由业务方书面确认后，开发方可启动编码。开发不可自行猜测。')

    questions = [
        ('Q1', '商品售价是否已包含服务费？', 'A. 包含 B. 单独展示'),
        ('Q2', '国际运费何时收取？', 'A. 下单时预估 B. 到仓后按实收'),
        ('Q3', '国际运费如何分摊到客户？', '按重量 / 按件数 / 按金额 / 均摊'),
        ('Q4', '客户能否合并多个商品为一个订单？', 'A. 可以 B. 不可'),
        ('Q5', '部分缺货处理方式？', 'A. 自动退款 B. 等待下一批'),
        ('Q6', '付款后未采购前能否取消？', 'A. 可以全额退 B. 不可取消'),
        ('Q7', '同一订单能否分多包裹发货？', 'A. 可以 B. 不可（合并发货）'),
        ('Q8', '物流信息录入方式？', 'A. 人工录入 B. 对接第三方 API'),
        ('Q9', '服务费率如何设定？', 'A. 固定金额 B. 按商品金额比例 C. 按 SKU 分别设置'),
        ('Q10', '国内快递费收取策略？', 'A. 包邮 B. 按订单金额门槛 C. 按重量'),
    ]
    add_data_table(doc, ['编号', '待确认事项', '选项'], questions,
                   col_widths=[Cm(2), Cm(6), Cm(8)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 10 章 验收标准
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 10 章  验收标准（Acceptance Criteria）', level=1)

    add_heading_with_style(doc, '10.1 核心验收用例', level=2)
    acceptance = [
        ('AC-001', '价格防篡改', '前端篡改金额提交订单', '后端拦截,按 SKU 最新价+服务费重算'),
        ('AC-002', '支付幂等', '重复发送同一笔微信支付回调', '系统只处理一次,不重复记账'),
        ('AC-003', '采购正向追溯', '输入采购批次号', '能查出该批次所有数量分配给了哪些订单'),
        ('AC-004', '采购反向追溯', '输入订单号', '能查到该订单商品来自哪个批次/物流'),
        ('AC-005', '部分退款状态', '支付 1000 元,缺货退款 200 元', '订单状态正确更新为"部分退款"'),
        ('AC-006', '退款权限隔离', '普通运营账号调用退款审核 API', '返回 403,无权限'),
        ('AC-007', '数据权限隔离', '普通运营账号访问他人订单', '返回 403,无权限'),
        ('AC-008', '采购分配防重', '同一批次同一 SKU 重复点击"分配"', '系统只处理一次,提示已分配'),
        ('AC-009', '用户无退款入口', '用户尝试在小程序发起退款', '无任何入口,API 调用直接拒绝'),
        ('AC-010', '异步导出', '导出 10 万订单的 Excel', '异步执行,完成后通知下载,不阻塞'),
    ]
    add_data_table(doc, ['编号', '验收点', '测试场景', '预期结果'], acceptance,
                   col_widths=[Cm(2), Cm(3), Cm(5), Cm(6)])

    add_heading_with_style(doc, '10.2 业务闭环验证用例', level=2)
    add_paragraph_text(doc,
        '以下用例验证业务闭环是否成立。每个用例都对应一个完整的业务场景，必须形成完整的开始、处理、收尾。')

    closed_loop_cases = [
        ('L-001', '完整订单闭环', '客户下单→支付→采购→发货→签收', '订单状态最终为"已完成",全链路可追溯'),
        ('L-002', '部分退款闭环', '客户下单→部分采购失败→后台退款', '退款成功,订单状态为"部分退款",剩余商品继续发货'),
        ('L-003', '完全失败闭环', '客户下单→采购完全失败→全额退款', '订单状态为"已退款",用户收到退款'),
        ('L-004', '多 SKU 订单闭环', '客户一次下单含 5 个 SKU', '5 个 SKU 独立采购分配,独立发货/退款'),
        ('L-005', '合并发货闭环', '同客户多订单商品合并发货', '所有订单共享同一国内包裹,物流同步'),
    ]
    add_data_table(doc, ['编号', '验收点', '测试场景', '预期结果'], closed_loop_cases,
                   col_widths=[Cm(2), Cm(3), Cm(5), Cm(6)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 第 11 章 项目交付清单
    # ------------------------------------------------------------
    add_heading_with_style(doc, '第 11 章  项目交付清单', level=1)

    add_heading_with_style(doc, '11.1 第一阶段交付物', level=2)
    deliverables = [
        ('1', '微信小程序（源码 + 体验版）', '用户端完整可运行'),
        ('2', 'Web 管理后台（源码 + 访问地址）', '运营、采购、仓库、财务使用'),
        ('3', '后端 API 服务（Docker 镜像 + 部署包）', '可一键启动'),
        ('4', '数据库设计文档（含 ER 图）', '详细建表脚本'),
        ('5', 'API 接口文档（Swagger / YAPI）', '前后端联调用'),
        ('6', '商品批量录入模板（Excel 模板）', '简化商品上架操作'),
        ('7', '部署文档 + 数据库备份恢复说明', '-'),
        ('8', '测试用例 + 测试报告', '覆盖所有 AC'),
        ('9', '源代码 Git 仓库权限', '必须控制在公司手中'),
        ('10', '运营手册（图文）', '后台操作指南'),
    ]
    add_data_table(doc, ['序号', '交付物', '说明'], deliverables,
                   col_widths=[Cm(2), Cm(7), Cm(7)])

    add_heading_with_style(doc, '11.2 第一阶段不在范围内', level=2)
    not_in_scope = [
        ('营销功能', '直播带货、社群裂变'),
        ('多语言', '仅支持中文'),
        ('多商家入驻', '仅自有业务'),
        ('跨境支付', '仅微信支付'),
        ('第三方物流 API 对接', '首期人工录入'),
    ]
    add_data_table(doc, ['范围', '说明'], not_in_scope,
                   col_widths=[Cm(5), Cm(11)])

    add_heading_with_style(doc, '11.3 已知风险', level=2)
    risks = [
        ('微信小程序审核', '上线可能延期', '提前预留资质,提前提交审核'),
        ('日本官网限购', '采购失败率上升', '系统支持限购异常处理,提供多渠道采购'),
        ('跨境物流时效不可控', '客户投诉风险', '物流实时跟踪,客服话术准备'),
        ('汇率波动', '采购成本变化', '实时采购款结算,价格风险定价'),
        ('采购集中度风险', '单一渠道问题影响全局', '建立备用采购渠道'),
    ]
    add_data_table(doc, ['风险', '影响', '应对'], risks,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 附录：术语表
    # ------------------------------------------------------------
    add_heading_with_style(doc, '附录 A  术语表', level=1)
    glossary = [
        ('SPU', 'Standard Product Unit', '标准化产品单元。一个品牌 + 款型 = 一个 SPU'),
        ('SKU', 'Stock Keeping Unit', '库存单元。具体规格组合（颜色 + 尺码）'),
        ('采购批次', 'Purchase Batch', '一次集中采购行为的记录'),
        ('采购分配表', 'Purchase Allocation', '灵魂表,记录每件商品去向'),
        ('采购异常', 'Purchase Exception', '缺货/限购/涨价等无法满足的采购情况'),
        ('订单快照', 'Order Snapshot', '下单时所有价格/规格/地址的不可变副本'),
        ('后端重算', 'Backend Recalculation', '前端传参不可信,后端必须重算金额'),
        ('幂等', 'Idempotent', '同一操作多次执行结果一致'),
        ('退款闭环', 'Refund Closed Loop', '从异常识别到用户收到退款的完整链路'),
        ('数据闭环', 'Data Closed Loop', '任何业务事件可追溯完整上下游'),
        ('状态机', 'State Machine', '实体所有可能状态的转换规则'),
        ('跨境直邮', 'Cross-border Direct Mail', '日本仓→国际物流→国内分发的发货模式'),
    ]
    add_data_table(doc, ['术语', '英文', '说明'], glossary,
                   col_widths=[Cm(3), Cm(5), Cm(8)])

    # ------------------------------------------------------------
    # 文档版本
    # ------------------------------------------------------------
    add_heading_with_style(doc, '附录 B  文档版本管理', level=1)
    add_data_table(doc, ['版本', '日期', '修改人', '修改内容'],
        [
            ('V1.0', '2026-10-12', '产品组', '首版建立,以业务闭环为核心设计原则'),
            ('V1.1', '2026-10-12', '产品组', '扩展增强版:新增 8.5 扩展性设计、附录 C 扩展点清单、附录 D 版本演进路线图'),
        ], col_widths=[Cm(2), Cm(3), Cm(3), Cm(8)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 附录 C：扩展点清单
    # ------------------------------------------------------------
    add_heading_with_style(doc, '附录 C  扩展点清单（V1.1 新增）', level=1)
    add_quote_block(doc,
        '本附录列出系统所有预留的扩展点。当业务需要调整时，优先使用扩展点实现，而不是修改核心代码。')

    add_heading_with_style(doc, 'C.1 商品域扩展点', level=2)
    product_ext = [
        ('商品分类', '一级分类可扩展为多级树', '运营自助维护'),
        ('商品标签', '预留 tags 字段', '商品打标、推荐'),
        ('商品规格', 'JSON 字段支持自定义规格', '非标品上架'),
        ('商品图片', '支持多图、视频', '富媒体展示'),
        ('价格规则', '会员价、促销价预留', '营销活动'),
        ('商品来源渠道', '枚举可扩展', '多渠道采购'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], product_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, 'C.2 订单域扩展点', level=2)
    order_ext = [
        ('订单扩展字段', 'ext_field_1 ~ 10', '业务标签、特殊标识'),
        ('订单备注', 'buyer_remark / seller_remark', '用户备注 + 运营备注'),
        ('订单类型', '枚举可扩展', '普通 / 团购 / 预售'),
        ('优惠规则', '预留 discount 字段', '优惠券、满减'),
        ('发票信息', '预留 invoice 字段', '企业用户开票'),
        ('订单合并规则', '策略模式可替换', '业务调整合并策略'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], order_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, 'C.3 支付域扩展点', level=2)
    pay_ext = [
        ('支付渠道', '抽象支付接口,可对接支付宝、银联', '多渠道支付'),
        ('支付方式', 'H5 / JSAPI / Native', '不同端使用不同支付方式'),
        ('退款渠道', '与支付渠道解耦', '支持部分退款'),
        ('分账规则', '预留分账字段', '二级分销'),
        ('账期管理', '预留账期字段', '对公账户、应收应付'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], pay_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, 'C.4 物流域扩展点', level=2)
    logistics_ext = [
        ('物流渠道', '抽象物流接口,可对接 SF / JD / YTO', '多物流公司'),
        ('运费计算', '策略模式 + 配置化', '业务调整运费规则'),
        ('运费分摊', '策略模式 + 配置化', '业务调整分摊逻辑'),
        ('轨迹同步', '接口抽象,可对接第三方 API', '实时轨迹'),
        ('包裹合并', '策略模式可调整', '业务调整合并规则'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], logistics_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, 'C.5 通知域扩展点', level=2)
    notif_ext = [
        ('通知模板', '模板化配置', '文案调整无需改代码'),
        ('通知渠道', '抽象通知接口,可扩展短信/邮件', '多渠道触达'),
        ('通知触发', '事件驱动 + 配置化', '运营策略调整'),
        ('用户触达频次', '配置化防骚扰', '用户体验'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], notif_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_heading_with_style(doc, 'C.6 财务域扩展点', level=2)
    fin_ext = [
        ('财务报表', '抽象报表引擎', '新增报表不影响核心'),
        ('财务对接', '预留对账接口', '对接外部 ERP'),
        ('币种', '预留 currency 字段', '多币种业务'),
        ('税率', '配置化', '跨境税率调整'),
        ('结算周期', '配置化', '与供应商结算'),
    ]
    add_data_table(doc, ['扩展点', '说明', '使用场景'], fin_ext,
                   col_widths=[Cm(4), Cm(5), Cm(7)])

    add_page_break(doc)

    # ------------------------------------------------------------
    # 附录 D：版本演进路线图
    # ------------------------------------------------------------
    add_heading_with_style(doc, '附录 D  版本演进路线图（V1.1 新增）', level=1)
    add_quote_block(doc,
        '本附录规划系统未来 18 个月的演进路径。每个版本预留扩展点，避免推翻重来。')

    add_heading_with_style(doc, 'D.1 演进总览', level=2)
    add_code_block(doc,
"""V1.0 (当前) ─基础版 ─单一代购 + 微信支付 + 人工物流
   │
   ├─ V1.1 (已发布) ─扩展增强版 ─补充扩展性设计
   │
V1.5 ─优化版 ─对接第三方物流 API + 运费实时计算 + 异步任务框架
   │
V2.0 ─多端版 ─多支付方式（支付宝/银联）+ 公众号/H5 端 + 多商家入驻
   │
V2.5 ─营销版 ─直播带货 + 社群裂变 + 优惠券 + 会员体系
   │
V3.0 ─智能版 ─AI 选品 + 智能定价 + 销量预测 + 自动化运营""")

    add_heading_with_style(doc, 'D.2 各版本详细规划', level=2)

    add_heading_with_style(doc, 'V1.5 优化版（建议 +3 个月）', level=3)
    v15 = [
        ('对接第三方物流 API', 'EMS / SF 国际 / YTO 实时轨迹', '替换人工录入'),
        ('运费实时计算', '按重量、目的地自动报价', '减少人工核算'),
        ('异步任务框架', 'XXL-JOB / Spring Task', '导出、对账、通知异步化'),
        ('性能优化', 'Redis 缓存 + SQL 优化', 'p99 全面达标'),
        ('运营配置后台', '运营自助修改服务费、运费规则', '减少开发介入'),
    ]
    add_data_table(doc, ['功能', '说明', '业务价值'], v15,
                   col_widths=[Cm(4), Cm(6), Cm(6)])

    add_heading_with_style(doc, 'V2.0 多端版（建议 +6 个月）', level=3)
    v20 = [
        ('多支付方式', '支付宝、银联、Apple Pay', '扩大用户覆盖'),
        ('公众号 / H5 端', '公众号入口、H5 商城', '多端获客'),
        ('多商家入驻', 'SaaS 化,支持其他代购商家', '商业模式升级'),
        ('商家管理后台', '独立商家后台', '多租户'),
        ('数据隔离', '按商家数据隔离', '安全合规'),
    ]
    add_data_table(doc, ['功能', '说明', '业务价值'], v20,
                   col_widths=[Cm(4), Cm(6), Cm(6)])

    add_heading_with_style(doc, 'V2.5 营销版（建议 +12 个月）', level=3)
    v25 = [
        ('直播带货', '小程序直播组件', '提升转化'),
        ('社群裂变', '分享助力、拼团', '拉新'),
        ('优惠券体系', '满减、折扣、品类券', '促销'),
        ('会员体系', '等级、积分、权益', '留存'),
        ('复购引导', '智能推荐 + 召回', '提升 LTV'),
    ]
    add_data_table(doc, ['功能', '说明', '业务价值'], v25,
                   col_widths=[Cm(4), Cm(6), Cm(6)])

    add_heading_with_style(doc, 'V3.0 智能版（建议 +18 个月）', level=3)
    v30 = [
        ('AI 选品', '基于历史销量推荐选品', '提升选品效率'),
        ('智能定价', '基于供需自动定价', '利润最大化'),
        ('销量预测', 'AI 预测未来销量', '采购决策'),
        ('自动化运营', '异常自动处理', '降低人工'),
        ('数据中台', '统一数据指标体系', '支撑业务决策'),
    ]
    add_data_table(doc, ['功能', '说明', '业务价值'], v30,
                   col_widths=[Cm(4), Cm(6), Cm(6)])

    add_heading_with_style(doc, 'D.3 演进原则', level=2)
    add_paragraph_text(doc, '为保证平滑演进，所有版本必须遵守以下原则：', bold=True)
    add_bullet(doc, '向后兼容：旧版本客户端/商家可继续使用')
    add_bullet(doc, '数据兼容：新旧版本数据可平滑迁移，不丢数据')
    add_bullet(doc, '接口兼容：API 至少向后兼容 2 个版本')
    add_bullet(doc, '配置兼容：业务规则调整通过配置实现，不改代码')
    add_bullet(doc, '模块可独立升级：单个模块升级不影响整体')

    add_heading_with_style(doc, 'D.4 技术债管理', level=2)
    add_paragraph_text(doc,
        '每个版本预留 20% 时间用于技术债偿还，避免长期累积导致系统不可维护。')
    tech_debt = [
        ('V1.5', '缓存体系完善、SQL 优化', '为 V2.0 性能瓶颈预防'),
        ('V2.0', '微服务拆分准备', '为 V2.5 多端支持铺路'),
        ('V2.5', '中台化重构', '为 V3.0 智能化准备'),
        ('V3.0', '数据中台建设', '为长期数据资产沉淀'),
    ]
    add_data_table(doc, ['版本', '技术债内容', '目标'], tech_debt,
                   col_widths=[Cm(3), Cm(7), Cm(6)])

    # 文档结束
    for _ in range(2):
        doc.add_paragraph()

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('—— 文档结束 ——')
    run.font.name = '微软雅黑'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # 保存
    doc.save(OUTPUT_PATH)
    print(f"文档已生成：{OUTPUT_PATH}")
    return OUTPUT_PATH


if __name__ == "__main__":
    build_document()
