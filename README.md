### Wrapper HFO env for reinforcement research.

Source environment comes from [HFO]( https://github.com/LARG/HFO ).

We wrap it  for the convenience of reinforcement learning research.

After build the project and pip install hfo, you can enjoy this wrapper by:

```python
import random
from env_wrapper import hfo_env

env = hfo_env(port=6006)

s = env.reset()
done = False

while not done:
    s_, r, done, _ = env.step(random.randint(0,4))
    s = s_
```