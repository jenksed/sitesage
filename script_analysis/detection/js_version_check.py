import logging

def check_js_versions(driver):
    versions = driver.execute_script("""
        var versions = [];
        if (window.jQuery) {
            versions.push(jQuery.fn.jquery);
        }
        return versions;
    """)
    logging.info(f"Checked JS versions: {versions}.")
    return versions
