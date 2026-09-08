#!/bin/sh
set -eu
if [ ! -d /data/logs ]; then mkdir -p /data/logs; if [ -d /seed/logs ]; then cp -a /seed/logs/. /data/logs/; fi; fi
if [ ! -d /data/final_reports ]; then mkdir -p /data/final_reports; if [ -d /seed/final_reports ]; then cp -a /seed/final_reports/. /data/final_reports/; fi; fi
if [ ! -d /data/insight_engine_streamlit_reports ]; then mkdir -p /data/insight_engine_streamlit_reports; if [ -d /seed/insight_engine_streamlit_reports ]; then cp -a /seed/insight_engine_streamlit_reports/. /data/insight_engine_streamlit_reports/; fi; fi
if [ ! -d /data/media_engine_streamlit_reports ]; then mkdir -p /data/media_engine_streamlit_reports; if [ -d /seed/media_engine_streamlit_reports ]; then cp -a /seed/media_engine_streamlit_reports/. /data/media_engine_streamlit_reports/; fi; fi
if [ ! -d /data/query_engine_streamlit_reports ]; then mkdir -p /data/query_engine_streamlit_reports; if [ -d /seed/query_engine_streamlit_reports ]; then cp -a /seed/query_engine_streamlit_reports/. /data/query_engine_streamlit_reports/; fi; fi
if [ ! -f /data/config.env ]; then printf "# Railway supplies environment defaults\n" > /data/config.env; fi
ln -sf /data/config.env /app/.env
exec "$@"
