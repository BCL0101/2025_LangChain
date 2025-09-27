"""
LangChain 專業翻譯 Agent - Gradio 介面
支援多語言翻譯、專業領域翻譯、語氣風格保持等功能
"""

import gradio as gr
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any
import os

class TranslationAgent:
    """專業翻譯 Agent"""
    
    def __init__(self):
        self.model = OllamaLLM(model="llama3.2:latest")
        self.translation_history = []
        
        # 支援的語言選項
        self.languages = {
            "繁體中文": "繁體中文",
            "简体中文": "简体中文", 
            "English": "英文",
            "日本語": "日文",
            "한국어": "韓文",
            "Français": "法文",
            "Deutsch": "德文",
            "Español": "西班牙文",
            "Italiano": "義大利文",
            "Português": "葡萄牙文"
        }
        
        # 專業領域選項
        self.domains = [
            "一般", "商業", "科技", "醫學", "法律", "學術", "文學", 
            "新聞", "行銷", "教育", "工程", "金融", "旅遊", "藝術"
        ]
        
        # 語氣風格選項
        self.tone_styles = [
            "正式", "友善", "專業", "輕鬆", "學術", "商務", "創意", "簡潔"
        ]
    
    def translate_text(self, source_text: str, source_language: str, 
                      target_language: str, domain: str, tone_style: str) -> Dict[str, Any]:
        """執行翻譯任務"""
        if not source_text.strip():
            return {
                "translation": "請輸入要翻譯的文本",
                "prompt": "",
                "status": "error"
            }
        
        try:
            # 建立翻譯模板
            complex_template = f"""
你是一位專業的{target_language}翻譯家，專精於{domain}領域，擅長{tone_style}風格的翻譯。
請將以下{source_language}文本翻譯成{target_language}，並確保：
1. 保持原文的語氣和風格（{tone_style}）
2. 使用{domain}領域的專業術語
3. 符合{target_language}的語言習慣
4. 保持原文的語義完整性
5. 提供自然流暢的翻譯結果

{source_language}文本：{{text}}
{target_language}翻譯：
"""
            
            chat_prompt_template = ChatPromptTemplate.from_template(complex_template)
            formatted_prompt = chat_prompt_template.format(text=source_text)
            
            # 執行翻譯
            response = self.model.invoke(formatted_prompt)
            translation_result = response if isinstance(response, str) else str(response)
            
            # 保存翻譯歷史
            translation_record = {
                "source_text": source_text,
                "source_language": source_language,
                "target_language": target_language,
                "domain": domain,
                "tone_style": tone_style,
                "translation": translation_result,
                "prompt": formatted_prompt
            }
            self.translation_history.append(translation_record)
            
            return {
                "translation": translation_result,
                "prompt": formatted_prompt,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "translation": f"翻譯過程中發生錯誤: {str(e)}",
                "prompt": "",
                "status": "error"
            }
    
    def get_translation_history(self) -> str:
        """取得翻譯歷史"""
        if not self.translation_history:
            return "尚無翻譯記錄"
        
        history_text = "# 📚 翻譯歷史記錄\n\n"
        for i, record in enumerate(self.translation_history[-10:], 1):  # 顯示最近10筆
            history_text += f"## {i}. {record['source_language']} → {record['target_language']}\n"
            history_text += f"**領域**: {record['domain']} | **風格**: {record['tone_style']}\n"
            history_text += f"**原文**: {record['source_text'][:100]}{'...' if len(record['source_text']) > 100 else ''}\n"
            history_text += f"**譯文**: {record['translation'][:150]}{'...' if len(record['translation']) > 150 else ''}\n\n"
        
        return history_text
    
    def clear_history(self):
        """清除翻譯歷史"""
        self.translation_history = []
        return "✅ 翻譯歷史已清除"

# 建立翻譯 Agent 實例
translation_agent = TranslationAgent()

def create_translation_interface():
    """建立翻譯介面"""
    
    with gr.Blocks(
        title="LangChain 專業翻譯 Agent",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            margin: auto !important;
        }
        
        /* 標題樣式 */
        .title {
            text-align: center !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            font-size: 2.5em !important;
            font-weight: bold !important;
            margin-bottom: 20px !important;
        }
        
        /* 卡片樣式 */
        .translation-card {
            background: linear-gradient(145deg, #ffffff, #f0f0f0) !important;
            border-radius: 20px !important;
            padding: 25px !important;
            margin: 15px 0 !important;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
        }
        
        /* 輸入框樣式 */
        .textbox {
            border-radius: 12px !important;
            border: 2px solid #e1e5e9 !important;
            transition: all 0.3s ease !important;
        }
        
        .textbox:focus {
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }
        
        /* 按鈕樣式 */
        .btn {
            border-radius: 12px !important;
            padding: 12px 24px !important;
            font-weight: 600 !important;
            transition: all 0.3s ease !important;
            border: none !important;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3) !important;
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
            color: white !important;
        }
        
        .btn-secondary:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.3) !important;
        }
        
        /* 下拉選單樣式 */
        .dropdown {
            border-radius: 8px !important;
            border: 2px solid #e1e5e9 !important;
        }
        
        /* 輸出區域樣式 */
        .output-text {
            background: linear-gradient(145deg, #f8f9fa, #ffffff) !important;
            border-radius: 12px !important;
            padding: 20px !important;
            border-left: 4px solid #667eea !important;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
            line-height: 1.6 !important;
        }
        
        /* 歷史記錄樣式 */
        .history-panel {
            background: linear-gradient(145deg, #ffffff, #f8f9fa) !important;
            border-radius: 16px !important;
            padding: 20px !important;
            border: 1px solid #e9ecef !important;
            max-height: 400px !important;
            overflow-y: auto !important;
        }
        
        /* 響應式設計 */
        @media (max-width: 768px) {
            .gradio-container {
                padding: 10px !important;
            }
            
            .translation-card {
                padding: 15px !important;
            }
        }
        """
    ) as interface:
        
        gr.HTML("""
        <div class="title">
            🌍 LangChain 專業翻譯 Agent
        </div>
        <div style="text-align: center; color: #666; margin-bottom: 30px; font-size: 1.1em;">
            🚀 支援多語言翻譯 | 🎯 專業領域適配 | ✨ 智能風格保持
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=3):
                # 翻譯設定區域
                with gr.Group():
                    gr.Markdown("### ⚙️ 翻譯設定")
                    
                    with gr.Row():
                        source_lang = gr.Dropdown(
                            choices=list(translation_agent.languages.keys()),
                            value="English",
                            label="🌐 來源語言",
                            info="選擇要翻譯的語言"
                        )
                        target_lang = gr.Dropdown(
                            choices=list(translation_agent.languages.keys()),
                            value="繁體中文",
                            label="🎯 目標語言",
                            info="選擇翻譯目標語言"
                        )
                    
                    with gr.Row():
                        domain = gr.Dropdown(
                            choices=translation_agent.domains,
                            value="一般",
                            label="📚 專業領域",
                            info="選擇翻譯的專業領域"
                        )
                        tone_style = gr.Dropdown(
                            choices=translation_agent.tone_styles,
                            value="專業",
                            label="🎨 語氣風格",
                            info="選擇翻譯的語氣風格"
                        )
                
                # 輸入區域
                with gr.Group():
                    gr.Markdown("### 📝 文本輸入")
                    source_text = gr.Textbox(
                        label="輸入要翻譯的文本",
                        placeholder="請輸入要翻譯的文本...",
                        lines=6,
                        max_lines=10
                    )
                
                # 操作按鈕
                with gr.Row():
                    translate_btn = gr.Button(
                        "🚀 開始翻譯", 
                        variant="primary",
                        size="lg"
                    )
                    clear_btn = gr.Button(
                        "🗑️ 清除", 
                        variant="secondary"
                    )
            
            with gr.Column(scale=2):
                # 翻譯結果區域
                with gr.Group():
                    gr.Markdown("### ✨ 翻譯結果")
                    translation_output = gr.Textbox(
                        label="翻譯結果",
                        lines=8,
                        interactive=False,
                        show_copy_button=True
                    )
                
                # 詳細資訊
                with gr.Group():
                    gr.Markdown("### 📋 詳細資訊")
                    prompt_output = gr.Textbox(
                        label="使用的 Prompt",
                        lines=6,
                        interactive=False,
                        show_copy_button=True
                    )
        
        # 歷史記錄區域
        with gr.Row():
            with gr.Column():
                with gr.Group():
                    gr.Markdown("### 📚 翻譯歷史")
                    with gr.Row():
                        history_btn = gr.Button("📖 查看歷史", variant="secondary")
                        clear_history_btn = gr.Button("🗑️ 清除歷史", variant="secondary")
                    
                    history_output = gr.Markdown(
                        "尚無翻譯記錄",
                        elem_classes=["history-panel"]
                    )
        
        # 事件處理函數
        def perform_translation(source_text, source_lang, target_lang, domain, tone_style):
            """執行翻譯"""
            result = translation_agent.translate_text(
                source_text, source_lang, target_lang, domain, tone_style
            )
            return result["translation"], result["prompt"]
        
        def clear_inputs():
            """清除輸入"""
            return "", "", ""
        
        def show_history():
            """顯示歷史記錄"""
            return translation_agent.get_translation_history()
        
        def clear_history():
            """清除歷史記錄"""
            translation_agent.clear_history()
            return "✅ 翻譯歷史已清除"
        
        # 綁定事件
        translate_btn.click(
            perform_translation,
            inputs=[source_text, source_lang, target_lang, domain, tone_style],
            outputs=[translation_output, prompt_output]
        )
        
        clear_btn.click(
            clear_inputs,
            outputs=[source_text, translation_output, prompt_output]
        )
        
        history_btn.click(
            show_history,
            outputs=[history_output]
        )
        
        clear_history_btn.click(
            clear_history,
            outputs=[history_output]
        )
    
    return interface

def main():
    """主函數"""
    print("🚀 啟動 LangChain 專業翻譯 Agent...")
    print("🌐 正在啟動 Web 介面...")
    
    interface = create_translation_interface()
    
    try:
        interface.launch(
            server_name="127.0.0.1",
            server_port=7861,
            share=False,
            show_error=True
        )
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")
        print("💡 請檢查 Ollama 是否正在運行，並確認模型已下載")

if __name__ == "__main__":
    main()