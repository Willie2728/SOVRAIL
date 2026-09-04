#!/usr/bin/env python3
import argparse,pathlib,shutil
p=argparse.ArgumentParser(description='Scaffold SOVRAIL into an existing asset')
p.add_argument('target'); p.add_argument('--python',action='store_true',default=True)
a=p.parse_args(); root=pathlib.Path(a.target).resolve(); root.mkdir(parents=True,exist_ok=True)
(root/'sovrail').mkdir(exist_ok=True)
base=pathlib.Path(__file__).resolve().parents[1]
shutil.copy2(base/'sdk/python/sovrail_client.py',root/'sovrail/sovrail_client.py')
env=root/'.env.sovrail.example'; shutil.copy2(base/'templates/sovrail.env.template',env)
readme=root/'SOVRAIL_INTEGRATION.md'
readme.write_text('''# SOVRAIL Integration\n\n1. Copy `.env.sovrail.example` values into your secret manager.\n2. Ask the SOVRAIL administrator for a scoped key for this asset.\n3. Import `sovrail/sovrail_client.py` and route external AI/service calls through SOVRAIL.\n4. Do not commit real provider keys or SOVRAIL keys.\n5. Prefer provider=`auto` so local-first/failover policy remains centralized.\n''')
print(f'SOVRAIL scaffold installed into {root}')
