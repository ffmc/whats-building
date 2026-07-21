-- Single source of truth for the classification taxonomy.
-- Consumed by classify.py (builds the prompt + tool enums) and aggregate.py
-- (emits taxonomy.json for the website). Re-runnable: clears then re-inserts.
DELETE FROM dim_taxonomy;

-- Categories: the FORM the repo takes.
INSERT INTO dim_taxonomy (axis, slug, label, description, grp, sort_order) VALUES
 ('category','web-app','Web App','a deployable web application or hosted service','apps',10),
 ('category','mobile-app','Mobile App','an iOS/Android/cross-platform mobile application','apps',20),
 ('category','desktop-app','Desktop App','a desktop/native GUI application','apps',30),
 ('category','cli-tool','CLI Tool','primarily run from the command line by a human','packages',40),
 ('category','library-sdk','Library / SDK','imported as a dependency by other code (libraries, SDKs, frameworks, API clients, MCP servers)','packages',50),
 ('category','plugin-extension','Plugin / Extension','extends a specific host product (browser/editor/IDE extensions, themes, mods, add-ons)','packages',60),
 ('category','dev-tooling','Dev Tooling','tooling that acts ON code or the build (linters, formatters, compilers-as-tools, test runners, debuggers, build systems)','tooling',70),
 ('category','data-infra','Data Infrastructure','databases, queues, pipelines, storage, data engineering systems','tooling',80),
 ('category','model-dataset','Model / Dataset','ML model weights, datasets, benchmarks, corpora — data rather than executable product','tooling',90),
 ('category','config-boilerplate','Config / Boilerplate','starters, templates, dotfiles, scaffolding, configuration collections','tooling',100),
 ('category','game','Game','games or game engines','content',110),
 ('category','docs-reference','Docs / Reference','curated lists, awesome-lists, guides, tutorials, learning materials — no runnable product of its own','content',120),
 ('category','unknown','Unknown','the description is missing or too vague to determine the form','escape',900),
 ('category','other','Other','the form is clear but fits none of the above','escape',910);

-- Domains: the SUBJECT the repo is about.
INSERT INTO dim_taxonomy (axis, slug, label, description, grp, sort_order) VALUES
 ('domain','ai-agents-mcp','AI Agents & MCP','LLM agents, agent frameworks/orchestration, MCP servers, agent skills, prompt tooling','ai',10),
 ('domain','llm-genai-apps','LLM / GenAI Apps','applications and interfaces built on LLMs (chatbots, RAG apps, copilots, image/text generation products)','ai',20),
 ('domain','ml-dl-research','ML / DL Research','model architectures, training, fine-tuning, inference engines, ML research code','ai',30),
 ('domain','computer-vision','Computer Vision','image/video understanding, detection, OCR, generation','ai',40),
 ('domain','audio-speech','Audio & Speech','speech recognition, TTS, music, audio processing','ai',50),
 ('domain','nlp-text','NLP & Text','natural language processing, tokenizers, translation, text analysis, search/retrieval over text, written-language datasets','ai',55),
 ('domain','robotics','Robotics','robots, drones, SLAM, autonomous systems, ROS','technical',60),
 ('domain','graphics-3d','Graphics & 3D','rendering, shaders, 3D, game engines, simulation graphics','technical',70),
 ('domain','embedded-iot','Embedded & IoT','firmware, microcontrollers, hardware, IoT devices','technical',80),
 ('domain','networking','Networking','proxies, VPNs, HTTP/DNS, protocols, distributed networking','technical',90),
 ('domain','compilers-languages','Compilers & Languages','programming languages, compilers, interpreters, parsers, type systems','technical',100),
 ('domain','observability','Observability','logging, tracing, metrics, monitoring, profiling','technical',110),
 ('domain','testing-qa','Testing & QA','testing frameworks, fuzzing, QA, benchmarking correctness','technical',120),
 ('domain','blockchain','Blockchain','crypto, web3, smart contracts, decentralised ledgers','technical',130),
 ('domain','devops-infra','DevOps & Infra','Kubernetes, containers, CI/CD, cloud provisioning, SRE','technical',140),
 ('domain','ui-frontend','UI / Frontend','UI components, design systems, styling, theming','technical',150),
 ('domain','security','Security','auth, pentesting, cryptography, privacy, vulnerability tooling','technical',160),
 ('domain','data-analytics','Data & Analytics','BI, dashboards, ETL, data warehousing, visualization','technical',170),
 ('domain','fintech','Fintech','money, payments, banking, budgeting, invoicing, trading','product',180),
 ('domain','health-fitness','Health & Fitness','health tracking, fitness, medical','product',190),
 ('domain','education','Education','learning, teaching, courses','product',200),
 ('domain','e-commerce','E-commerce','online retail, marketplaces, storefronts','product',210),
 ('domain','social-communication','Social & Communication','chat, social networks, messaging, email','product',220),
 ('domain','gaming-entertainment','Gaming & Entertainment','playing games, media consumption, entertainment','product',230),
 ('domain','productivity','Productivity','task/project management, workflow automation, office work','product',240),
 ('domain','note-taking-pkm','Notes & PKM','notes, personal knowledge management, wikis','product',250),
 ('domain','content-media','Content & Media','content creation, publishing, video/image editing','product',260),
 ('domain','unknown','Unknown','the description is missing or too vague to determine the subject','escape',900),
 ('domain','other','Other','the subject is clear but fits none of the above','escape',910);
