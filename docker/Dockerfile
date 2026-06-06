#==============================================================================#
# Competition Workspace 用 閉じた実行環境イメージ "claude"
#
#   - GPU 対応 PyTorch + ML 一式 + Claude Code CLI を1枚に焼いた配布用イメージ。
#   - ビルド:  bash docker/build.sh           （ホストの UID/GID を引き継ぐ）
#   - 起動:    bash rundocker.sh               （リポジトリ直下で）
#
#   ※ ホスト固有の設定（マウントするドライブ等）は Dockerfile には書かず、
#     rundocker.sh 側で環境変数で渡す。イメージはどのマシンでも同じものになる。
#==============================================================================#

#------------------------------------------------------------------------------#
# 1) Build args (FROM の前)  ※FROM で使うため
#    ベースを PyTorch 2.7.1 / CUDA 12.8 / cuDNN 9 に統一
#------------------------------------------------------------------------------#
ARG PYTORCH="2.7.1"
ARG CUDA="12.8"
ARG CUDNN="9"

# GPU 対応の PyTorch ベース（torch 2.7.1 + cu128 を同梱）
FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel

LABEL org.opencontainers.image.title="competition-workspace" \
      org.opencontainers.image.description="Closed env: PyTorch + ML stack + Claude Code CLI" \
      org.opencontainers.image.source="https://github.com/"

#------------------------------------------------------------------------------#
# 2) Build args を FROM の「後」に再宣言
#------------------------------------------------------------------------------#
ARG NODE_MAJOR="22"        # 22 は現行 LTS。より新しい LTS が要れば 24 へ
ARG USERNAME="user"
ARG UID="1000"
ARG GID="1000"

ENV DEBIAN_FRONTEND=noninteractive

#------------------------------------------------------------------------------#
# 3) 基本ツール + Node.js（NodeSource）
#    ※ 旧版で重複していた ca-certificates / curl / git 等をここに集約
#------------------------------------------------------------------------------#
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates curl gnupg git bash build-essential \
      unzip zip vim openssh-client sudo; \
    curl -fsSL https://deb.nodesource.com/setup_${NODE_MAJOR}.x | bash -; \
    apt-get install -y --no-install-recommends nodejs; \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------------------#
# 4) GUI / OpenGL / Vulkan 系ライブラリ（+ wslu）
#    ※ Ubuntu 24.04 ベースに変えた場合は libasound2 → libasound2t64
#------------------------------------------------------------------------------#
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      x11-apps mesa-utils \
      libx11-6 libxext6 libxrender1 libxrandr2 libxfixes3 libxi6 \
      libxkbcommon0 libnss3 libasound2 libxss1 \
      libgtk-3-0 libgbm1 libdrm2 libxshmfence1 \
      libxft2 \
      mesa-vulkan-drivers \
      wslu; \
    rm -rf /var/lib/apt/lists/*

#------------------------------------------------------------------------------#
# 5) 日本語ロケール & フォント
#    ※ matplotlibrc で IPAexGothic を使うので fonts-ipaexfont を追加（旧版は
#      IPA(=IPAGothic) のみで IPAexGothic が無く効かない可能性があった）
#------------------------------------------------------------------------------#
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      locales fontconfig \
      fonts-noto-cjk fonts-noto-color-emoji \
      fonts-ipafont-gothic fonts-ipafont-mincho \
      fonts-ipaexfont-gothic fonts-ipaexfont-mincho; \
    sed -i 's/^# *ja_JP.UTF-8/ja_JP.UTF-8/' /etc/locale.gen; \
    locale-gen; \
    update-locale LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja LC_ALL=ja_JP.UTF-8; \
    fc-cache -f; \
    rm -rf /var/lib/apt/lists/*

ENV LANG=ja_JP.UTF-8 LANGUAGE=ja_JP:ja LC_ALL=ja_JP.UTF-8

#------------------------------------------------------------------------------#
# 6) 非 root ユーザー作成 + sudo（NOPASSWD）
#------------------------------------------------------------------------------#
RUN set -eux; \
    if ! getent group "${GID}" >/dev/null; then groupadd -g "${GID}" "${USERNAME}"; fi; \
    if ! getent passwd "${UID}" >/dev/null; then useradd -m -u "${UID}" -g "${GID}" -s /bin/bash "${USERNAME}"; fi; \
    mkdir -p /home/${USERNAME}/.npm-global /workspace; \
    chown -R "${UID}:${GID}" /home/${USERNAME} /workspace; \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME}; \
    chmod 0440 /etc/sudoers.d/${USERNAME}

#------------------------------------------------------------------------------#
# 7) Python packages（torch はベース同梱なので再インストールしない）
#    ※ opencv-python と opencv-contrib-python の重複を contrib 一本に整理
#------------------------------------------------------------------------------#
RUN set -eux; \
    pip install --no-cache-dir \
      scipy opencv-contrib-python \
      pandas tqdm albumentations scikit-learn seaborn

#------------------------------------------------------------------------------#
# 8) Claude Code を「システム側」に導入（root グローバル）
#    ※ /home/${USERNAME} に置くと、起動時に作業フォルダを /home にマウントした
#      際に隠れて消える。システム側 (/usr/...) に入れておけば上書きされない。
#    ※ NPM_CONFIG_PREFIX を設定する「前」に入れること（前に置かないとユーザー
#      ホーム配下に入ってしまう）。
#------------------------------------------------------------------------------#
RUN npm i -g --no-audit --omit=dev @anthropic-ai/claude-code

#------------------------------------------------------------------------------#
# 9) matplotlib の既定フォントを日本語に（システム側に置く）
#    ※ 設定ファイルは読み取り専用でよいので /opt に置き MATPLOTLIBRC で指定。
#      フォントキャッシュは ~/.cache に作られる（＝永続化対象のホーム側）。
#------------------------------------------------------------------------------#
RUN set -eux; \
    mkdir -p /opt/mpl; \
    printf "%s\n" \
      "font.family: IPAexGothic" \
      "axes.unicode_minus: False" \
      > /opt/mpl/matplotlibrc
ENV MATPLOTLIBRC=/opt/mpl/matplotlibrc

#------------------------------------------------------------------------------#
# 10) user 環境（PATH / 後から入れる物はホーム配下＝永続化対象に）
#     ※ ユーザーが後で行う pip install --user → ~/.local、npm -g → ~/.npm-global。
#       いずれも /home/${USERNAME} 配下なので、ホームを作業フォルダにマウント
#       すれば永続する。
#------------------------------------------------------------------------------#
# pip install を既定で --user 相当に（→ ~/.local に入り永続化される）
#   ※ build 時(セクション7)の root インストールはこの行より前なので影響なし。
#   ※ venv を使うときは PIP_USER=1 だと venv 内 pip がエラーになるため、
#     その場合だけ `PIP_USER=0 pip install ...` か `pip install --no-user` で回避。
ENV PIP_USER=1
ENV NPM_CONFIG_PREFIX=/home/${USERNAME}/.npm-global
ENV PATH=/home/${USERNAME}/.local/bin:/home/${USERNAME}/.npm-global/bin:$PATH

WORKDIR /workspace
USER ${USERNAME}
