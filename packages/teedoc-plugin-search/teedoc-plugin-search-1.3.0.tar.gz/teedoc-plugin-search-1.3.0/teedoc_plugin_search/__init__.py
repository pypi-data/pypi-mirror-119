from genericpath import exists
import os, sys
from os.path import join
import tempfile
import shutil
import json
import copy
try:
    curr_path = os.path.dirname(os.path.abspath(__file__))
    teedoc_project_path = os.path.abspath(os.path.join(curr_path, "..", "..", ".."))
    if os.path.basename(teedoc_project_path) == "teedoc":
        sys.path.insert(0, teedoc_project_path)
except Exception:
    pass
from teedoc import Plugin_Base
from teedoc import Fake_Logger
from teedoc.utils import update_config

__version__ = "1.3.0"

class Plugin(Plugin_Base):
    name = "teedoc-plugin-search"
    desc = "search support for teedoc"
    defautl_config = {
        "content_type": "raw", # supported_content_type
        "search_hint" : "Search",
        "input_hint" : "Keywords separated by space",
        "loading_hint" : "Loading, wait please ...",
        "download_err_hint" : "Download error, please check network and refresh again",
        "other_docs_result_hint" : "Result from other docs",
        "curr_doc_result_hint" : "Result from current doc"
    }
    supported_content_type = ["raw", "html"]

    def on_init(self, config, doc_src_path, site_config, logger = None):
        '''
            @config a dict object
            @logger teedoc.logger.Logger object
        '''
        self.logger = Fake_Logger() if not logger else logger
        self.doc_src_path = doc_src_path
        self.site_config = site_config
        self.config = Plugin.defautl_config
        self.config.update(config)
        self.logger.i("-- plugin <{}> init".format(self.name))
        self.logger.i("-- plugin <{}> config: {}".format(self.name, self.config))
        if not self.config["content_type"] in self.supported_content_type:
            self.logger.e("-- plugin <{}> config content_type error: {}, should be in {}".format(self.name, self.config["content_type"], self.supported_content_type))
        if self.config["content_type"] == "raw":
            self.content_from = "raw"
        else:
            self.content_from = "body"
        self.module_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))
        self.assets_abs_path = os.path.join(self.module_path, "assets")
        self.temp_dir = os.path.join(tempfile.gettempdir(), "teedoc_plugin_search")
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

        self.css = {
            "/static/css/search/style.css": os.path.join(self.assets_abs_path, "style.css"),
        }
        self.footer_js = {
            "/static/js/search/search_main.js": os.path.join(self.assets_abs_path, "search_main.js")
        }
        self.images = {
            "/static/image/search/close.svg": os.path.join(self.assets_abs_path, "close.svg"),
            "/static/image/search/search.svg": os.path.join(self.assets_abs_path, "search.svg"),
        }
        
        # set site_root_url env value
        if not "env" in config:
            config['env'] = {}
        config['env']["site_root_url"] = self.site_config["site_root_url"]
        # replace variable in css with value
        vars = config["env"]
        self.css       = self._update_file_var(self.css, vars, self.temp_dir)
        self.footer_js = self._update_file_var(self.footer_js, vars, self.temp_dir)
        # files to copy
        self.html_header_items = self._generate_html_header_items()
        self.files_to_copy = {}
        self.files_to_copy.update(self.css)
        self.files_to_copy.update(self.footer_js)
        self.files_to_copy.update(self.images)

        self.html_js_items = self._generate_html_js_items()
        self.content = {
            "articles": {},
            "pages": {}
        }

    def on_del(self):
        if os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
            except Exception:
                pass

    def _generate_html_header_items(self):
        items = []
        # css
        for url in self.css:
            item = '<link rel="stylesheet" href="{}" type="text/css"/>'.format(url)
            items.append(item)
        return items

    def _generate_html_js_items(self):
        items = []
        for url in self.footer_js:
            item = '<script src="{}"></script>'.format(url)
            items.append(item)
        return items

    def _update_file_var(self, files, vars, temp_dir):
        for url, path in files.items():
            with open(path, encoding='utf-8') as f:
                content = f.read()
                for k, v in vars.items():
                    content = content.replace("${}{}{}".format("{", k.strip(), "}"), v)
                temp_path = os.path.join(temp_dir, os.path.basename(path))
                with open(temp_path, "w", encoding='utf-8') as fw:
                    fw.write(content)
                files[url] = temp_path
        return files

    def on_parse_start(self, type_name, doc_config, new_config):
        self.doc_locale = doc_config["locale"] if "locale" in doc_config else None
        self.new_config = copy.deepcopy(self.config)
        self.new_config = update_config(self.new_config, new_config)

    def on_add_html_header_items(self, type_name):
        return self.html_header_items
    
    def on_add_html_footer_js_items(self, type_name):
        return self.html_js_items
    
    def on_add_navbar_items(self):
        '''
            @config config cover self.config
        '''
        # i18n
        have_i18n = False
        if self.doc_locale:
            import gettext
            try:
                lang = gettext.translation('messages', localedir=os.path.join(self.module_path, 'locales'), languages=[self.doc_locale])
                lang.install()
                _ = lang.gettext
                have_i18n = True
                search_hint = _("search_hint")
                search_input_hint = _("search_input_hint")
                search_loading_hint = _("search_loading_hint")
                search_download_err_hint = _("search_download_err_hint")
                search_other_docs_result_hint = _("search_other_docs_result_hint")
                search_curr_doc_result_hint = _("search_curr_doc_result_hint")
            except Exception as e:
                pass
        if not have_i18n: # locale not set, default from self.new_config
            search_hint = self.new_config["search_hint"]
            search_input_hint = self.new_config["input_hint"]
            search_loading_hint = self.new_config["loading_hint"]
            search_download_err_hint = self.new_config["download_err_hint"]
            search_other_docs_result_hint = self.new_config["other_docs_result_hint"]
            search_curr_doc_result_hint = self.new_config["curr_doc_result_hint"] 
        search_btn = '''<a id="search"><span class="icon"></span><span class="placeholder">{}</span>
                            <div id="search_hints">
                                <span id="search_input_hint">{}</span>
                                <span id="search_loading_hint">{}</span>
                                <span id="search_download_err_hint">{}</span>
                                <span id="search_other_docs_result_hint">{}</span>
                                <span id="search_curr_doc_result_hint">{}</span>
                            </div></a>'''.format(search_hint, search_input_hint, search_loading_hint, search_download_err_hint, search_other_docs_result_hint, search_curr_doc_result_hint)
        items = [search_btn]
        return items
    
    def on_copy_files(self):
        res = self.files_to_copy
        self.files_to_copy = {}
        return res

    def on_htmls(self, htmls_files, htmls_pages, htmls_blog=None):
        '''
            update htmls, may not all html, just partially
            htmls_files: {
                "/get_started/zh":{
                    "url":{
                                "title": "",
                                "desc": "",
                                "keywords": [],
                                "body": html,
                                "url": "",
                                "raw": ""
                          }
                }
            }
        '''
        # for file, html in htmls_files.items():
        #     self.content["articles"][html["url"]] = html["raw"]
        # for file, html in htmls_pages.items():
        #     self.content["pages"][html["url"]] = html["raw"]
        self.logger.i("generate search index")
        if htmls_blog:
            htmls_pages.update(copy.deepcopy(htmls_blog))
        docs_url = list(htmls_files.keys())
        pages_url = list(htmls_pages.keys())
        index_content = {}
        sub_index_path = []
        generated_index_json = {}
        for i, url in enumerate(docs_url):
            index_content[url] = "{}static/search_index/index_{}.json".format(self.site_config["site_root_url"], i)
            path = os.path.join(self.temp_dir, "index_{}.json".format(i))
            sub_index_path.append(path)
            #   write content to sub index file
            content = {}
            for page_url in htmls_files[url]:
                content[page_url] = {
                    "title": htmls_files[url][page_url]["title"],
                    "content": htmls_files[url][page_url][self.content_from]
                }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False)
        for i, url in enumerate(pages_url, len(docs_url)):
            index_content[url] = "{}static/search_index/index_{}.json".format(self.site_config["site_root_url"], i)
            path = os.path.join(self.temp_dir, "index_{}.json".format(i))
            sub_index_path.append(path)
            #   write content to sub index file
            content = {}
            for page_url in htmls_pages[url]:
                content[page_url] = {
                    "title": htmls_pages[url][page_url]["title"],
                    "content": htmls_pages[url][page_url][self.content_from]
                }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False)
        # write content to files
        #   index file
        index_path = os.path.join(self.temp_dir, "index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(index_content, f, ensure_ascii=False)

        # add to copy file list
        generated_index_json["/static/search_index/index.json"] = index_path
        for i, path in enumerate(sub_index_path):
            generated_index_json["/static/search_index/index_{}.json".format(i)] = path
        self.files_to_copy.update(generated_index_json)
        return True
        



if __name__ == "__main__":
    config = {
    }
    plug = Plugin(config=config)

