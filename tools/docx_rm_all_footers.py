from docx import Document

"""
    docx 清空页脚内容
    # pip install python-docx
"""
def remove_all_footers(docx_file):
    # 打开 Word 文档
    doc = Document(docx_file)

    # 遍历所有节(section)
    for section in doc.sections:
        # 移除页脚
        footer = section.footer
        if footer is not None:
            for paragraph in footer.paragraphs:
                for run in paragraph.runs:
                    run.clear()  # 清空页脚内容

    # 保存修改并关闭文档
    doc.save(docx_file)


# 调用函数并传入 Word 文档路径
remove_all_footers("7_tec.docx")