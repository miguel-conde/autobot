from utils.chatbot import ChatBot
import argparse

from utils import globalsettings as gs


def get_args():
    
    parser = argparse.ArgumentParser(description="Simple chatbot")
    parser.add_argument(
        "--model", 
        help    = "OpenAI's model to use",
        default = gs.prj_cfg.default_model
        )
    parser.add_argument(
        "--personality",
        type    = str, 
        help    = "A brief summary of the chatbot's personality",
        default = gs.prj_cfg.default_directiva
        )
    args = parser.parse_args()
    print(f"Using {args.model}")
    
    return args


def main():
    
    args = get_args()
    print(args.personality)
    
    cb = ChatBot(
        model                 = args.model, 
        directiva_del_sistema = args.personality, 
        max_tokens            = int(gs.prj_cfg.default_max_tokens), 
        max_tokens_contexto   = int(gs.prj_cfg.default_max_tokens_contexto)
        )
    print(cb.cm.get_history())
#
    cb.run_chatbot()
#
    #cb.cm.print_history()
#
    #conversacion = cb.cm.get_history()
#
    #print(conversacion)

if __name__ == "__main__":
    main()