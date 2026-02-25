class Analyzer:

    def analyze(self, mode_result):
        """
        Entry point: auto-detect mode type and analyze accordingly.
        """
        mode = mode_result.get("mode")

        if mode == "dns_mode":
            return self.analyze_dns(mode_result)

        if mode == "redirect_mode":
            return self.analyze_redirects(mode_result)

        if mode == "metadata_mode":
            return self.analyze_metadata(mode_result)

        if mode == "header_probe_mode":
            return self.analyze_headers(mode_result)

        if mode == "file_mode":
            return self.analyze_file(mode_result)

        if mode == "gopher_mode":
            return self.analyze_gopher(mode_result)

        if mode == "raw_socket_mode":
            return self.analyze_raw_socket(mode_result)

        if mode == "smuggling_mode":
            return self.analyze_smuggling(mode_result)

        # Modes that intentionally produce no analyzable signals
        if mode in ("mode_d", "template"):
            return {"info": f"Mode '{mode}' does not require analysis."}

        return {"error": f"No analyzer available for mode '{mode}'"}

    # -------------------------------------------------------------
    # DNS MODE
    # -------------------------------------------------------------
    def analyze_dns(self, result):
        return {
            "resolver": result.get("resolver"),
            "timing_ms": result.get("timing_ms"),
            "cached": result.get("cached"),
            "anomaly": result.get("timing_ms", 0) > 500
        }

    # -------------------------------------------------------------
    # REDIRECT MODE
    # -------------------------------------------------------------
    def analyze_redirects(self, result):
        chain = result.get("redirect_chain", [])
        return {
            "redirect_count": len(chain),
            "final_url": chain[-1] if chain else None,
            "loop_detected": len(chain) > 0 and chain[0] == chain[-1]
        }

    # -------------------------------------------------------------
    # METADATA MODE
    # -------------------------------------------------------------
    def analyze_metadata(self, result):
        meta = result.get("metadata", {})
        return {
            "keys_found": list(meta.keys()),
            "sensitive": any(k.lower() in ("token", "key", "secret") for k in meta)
        }

    # -------------------------------------------------------------
    # HEADER PROBE MODE
    # -------------------------------------------------------------
    def analyze_headers(self, result):
        headers = result.get("headers", {})
        return {
            "header_count": len(headers),
            "interesting": [h for h in headers if h.lower().startswith("x-")]
        }

    # -------------------------------------------------------------
    # FILE MODE
    # -------------------------------------------------------------
    def analyze_file(self, result):
        return {
            "size": len(result.get("content", "")),
            "contains_html": "<html" in result.get("content", "").lower()
        }

    # -------------------------------------------------------------
    # GOPHER MODE
    # -------------------------------------------------------------
    def analyze_gopher(self, result):
        resp = result.get("response", "")
        return {
            "response_length": len(resp),
            "contains_banner": "\n" in resp or ":" in resp
        }

    # -------------------------------------------------------------
    # RAW SOCKET MODE
    # -------------------------------------------------------------
    def analyze_raw_socket(self, result):
        resp = result.get("response")
        return {
            "received_data": resp is not None,
            "response_length": len(resp) if resp else 0,
            "timing_ms": result.get("duration_ms")
        }

    # -------------------------------------------------------------
    # SMUGGLING MODE
    # -------------------------------------------------------------
    def analyze_smuggling(self, result):
        raw = result.get("raw", "")
        return {
            "payload_size": len(raw),
            "encoded_size": len(result.get("encoded", "")),
            "contains_chunked": "chunked" in raw.lower(),
            "contains_dual_cl": raw.lower().count("content-length") > 1
        }
