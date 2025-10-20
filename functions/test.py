# bot_cli.py
from openai import OpenAI
import os

def main():
    api_key = os.getenv("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")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY environment variable first.")
    client = OpenAI(api_key=api_key)

    system_prompt = "Bạn là một trợ lý thân thiện, trả lời ngắn gọn, rõ ràng bằng tiếng Việt."
    conversation = [
        {"role":"system", "content": system_prompt}
    ]

    print("Chat bot (gõ 'exit' để thoát)\n")
    while True:
        user_input = input("Bạn: ").strip()
        if user_input.lower() in ("exit", "quit"):
            break
        conversation.append({"role":"user", "content": user_input})

        # Tạo completion chat
        resp = client.chat.completions.create(
            model="gpt-5-mini",     # hoặc model bạn có quyền dùng, ví dụ "gpt-4o" / "gpt-5-mini"
            messages=conversation,
            max_tokens=600
        )

        assistant_msg = resp.choices[0].message["content"]
        print("Bot:", assistant_msg.strip())
        conversation.append({"role":"assistant", "content": assistant_msg})

if __name__ == "__main__":
    main()
