"""Keep Responses instruction messages ahead of user input for SiliconFlow."""
from litellm.integrations.custom_logger import CustomLogger


class SystemFirst(CustomLogger):
    async def async_pre_call_hook(self, user_api_key_dict, cache, data, call_type):
        for field in ("input", "messages"):
            items = data.get(field)
            if isinstance(items, list):
                instructions = [m for m in items if isinstance(m, dict) and m.get("role") in ("system", "developer")]
                others = [m for m in items if not (isinstance(m, dict) and m.get("role") in ("system", "developer"))]
                texts = []
                for item in instructions:
                    content = item.get('content', '')
                    if isinstance(content, str):
                        texts.append(content)
                    elif isinstance(content, list):
                        texts.extend(part['text'] for part in content if isinstance(part, dict) and isinstance(part.get('text'), str))
                if field == 'input':
                    data[field] = others
                    if texts:
                        data['instructions'] = '\n\n'.join([data.get('instructions', ''), *texts]).strip()
                else:
                    data[field] = ([{'role':'system','content':'\n\n'.join(texts)}] if texts else []) + others
        return data


system_first = SystemFirst()
