import providers
import json

SYSTEM_PROMPT = """You are RECON BUDDY, a master of reconnaissance and ethical hacking. You are tasked with providing advice on how to perform
reconnaissance and ethical hacking tasks for a given target.
1. Read through all the information provided from various tools and advise on possible exploits and vulnerabilities or further reconnaissance tasks."""

def gather_information(info_dict):
    full_context = json.dumps(info_dict)
    for url in info_dict['crawl_results']['urls']:


    return full_context

def get_advise_from_buddy(info_dict):
    full_context = gather_information(info_dict)
    advise = providers.generate_openai_response(system_role=SYSTEM_PROMPT, user_prompt=full_context)
    return advise