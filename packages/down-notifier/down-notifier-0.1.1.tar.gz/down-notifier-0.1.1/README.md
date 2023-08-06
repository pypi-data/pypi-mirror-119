# Down notifier

## Usage

```bash
python -m down-notifier <config.json>
```

Example json config in "examples" folder.

```python
from down_notifier import Checker, Site
from down_notifier.channel import TelegramChannel

channel = TelegramChannel(
  name="channel_name",
  message="{} - {}",
  token="token",
  chats=["chat_id_1", "chat_id_2"],
)
site = Site(
  name="site_name",
  url="http://example.com",
  status_code=200,
  timeout=60,
  channels=[channel],
)
checker = Checker([site])

checker.start_loop()
```
