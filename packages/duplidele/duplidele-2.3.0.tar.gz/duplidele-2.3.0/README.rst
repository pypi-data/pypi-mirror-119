Introduce
=========

| Hi! Thanks for comming my site.
| When you want to delete duplicate sentence from your sentence, Please
  use duplidele.

How to install
==============

pip install duplidele

How to coding
=============

1)Delete one character at a time

| import duplidele as dd
| dd.exduplidelechar(“test sentence test sentence duplicate delete”, 5)

export ⇒test sentence duplicate delete

2)Delete word by word

| import duplidele as dd
| dd.exduplidele(“おはよう。元気ですか？おはよう。元気ですか？猫さん。私は元気です。”,
  6)

export ⇒ おはよう。元気ですか？猫さん。私は元気です。

| import duplidele as dd
| dd.exduplidele(“おはよう。元気ですか？おはよう。元気ですか？猫さん。私は元気です。”,
  7)

export ⇒
おはよう。元気ですか？おはよう。元気ですか？猫さん。私は元気です。

| import duplidele as dd
| dd.exduplidele(“おはよう。元気ですか？うん、おはよう。元気ですか？猫さん。私は元気です。”,
  6)

export ⇒
おはよう。元気ですか？おはよう。元気ですか？猫さん。私は元気です。

License
=======

MIT
