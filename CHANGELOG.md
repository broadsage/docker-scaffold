<!--
SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>

SPDX-License-Identifier: Apache-2.0
-->

# Changelog

## [2.1.0](https://github.com/broadsage/docker-scaffold/compare/v2.0.0...v2.1.0) (2025-12-23)


### Features

* Add SPDX headers to changelog ([8174735](https://github.com/broadsage/docker-scaffold/commit/81747352c38b739df97f3bebe92643790bb15874))
* Add SPDX headers to changelog ([8174735](https://github.com/broadsage/docker-scaffold/commit/81747352c38b739df97f3bebe92643790bb15874))
* add SPDX headers to CHANGELOG.md and template ([f6aa579](https://github.com/broadsage/docker-scaffold/commit/f6aa579d4cf6baf0bd24b0955715b32bf64fc9c6))
* **ci:** add Trivy container scanning to PR workflow ([66cb9a1](https://github.com/broadsage/docker-scaffold/commit/66cb9a186c94a5e3f0e53dbd9a2b6f43e7203c92))


### Bug Fixes

* remove abc user reference from ansible roles ([aed0a1c](https://github.com/broadsage/docker-scaffold/commit/aed0a1c8f64f8ed12e517852aaae91eecf7889d9))


### Code Refactoring

* remove Trivy scan from compliance workflow ([8fffea7](https://github.com/broadsage/docker-scaffold/commit/8fffea7f45ea57534ccd569b479f0bc698a99e55))

## [2.0.0](https://github.com/broadsage/docker-scaffold/compare/v1.0.0...v2.0.0) (2025-12-22)


### ⚠ BREAKING CHANGES

* Dependency management has been migrated from Dependabot to Renovate

### Features

* add ANSI colors to post-gen script output ([aab83d5](https://github.com/broadsage/docker-scaffold/commit/aab83d5f2b6f70dfe74aba2a0e2fc0fdd052999b))
* add ansible 2.20 to project dependencies ([e80cd54](https://github.com/broadsage/docker-scaffold/commit/e80cd5448e71edf4a0e650cf6ba1b4bf7722daf1))
* add automated release management with Release Please ([c2951e2](https://github.com/broadsage/docker-scaffold/commit/c2951e260256ca78f86ee6cd52aa76e3ab79b421))
* add comprehensive compliance workflow with quality gates ([0a034d7](https://github.com/broadsage/docker-scaffold/commit/0a034d7eff41809019c0a8488b147cf6b7e3c013))
* add comprehensive GitHub issue templates ([896b536](https://github.com/broadsage/docker-scaffold/commit/896b5367eddcca09e92172637e7477124a66ecd3))
* add comprehensive security policy for docker-scaffold ([3a053ef](https://github.com/broadsage/docker-scaffold/commit/3a053ef9c11dd35b8de58370c7c85609abff72e0))
* add cookiecutter support for project.yaml file generation ([c517e32](https://github.com/broadsage/docker-scaffold/commit/c517e32feb133ff401c22baee3b0a512eb088302))
* add cookiecutter support for the project generation ([fbbb4e4](https://github.com/broadsage/docker-scaffold/commit/fbbb4e4629c56877286773eeb7f9778b1b3443dd))
* add cookiecutter support for the project generation ([fbbb4e4](https://github.com/broadsage/docker-scaffold/commit/fbbb4e4629c56877286773eeb7f9778b1b3443dd))
* add date to timestamp in post-gen output ([e67140a](https://github.com/broadsage/docker-scaffold/commit/e67140a9db36cb77510ecc765e65abc7a2db5c91))
* add descriptive options to feature flags and update conditionals ([af0185f](https://github.com/broadsage/docker-scaffold/commit/af0185f658bdeaa3939cf5cd2396e4b83e43159d))
* add docker & lint best practices ([5681715](https://github.com/broadsage/docker-scaffold/commit/5681715680f9a758f1c02d7842bde43b031a8979))
* add docker-build target to Taskfile ([9ea534b](https://github.com/broadsage/docker-scaffold/commit/9ea534b0b897be11c88d71a28d52ee6832d22f04))
* add github discussion templates to project ([2cc7b96](https://github.com/broadsage/docker-scaffold/commit/2cc7b96a3c9ea361044f717933e537e11d3695d7))
* add GitHub Projects integration to issue templates ([b9ba301](https://github.com/broadsage/docker-scaffold/commit/b9ba3018e197cf18325e38da3fd2bc8976fdb874))
* add help and announcements discussion templates ([035606e](https://github.com/broadsage/docker-scaffold/commit/035606e8ab9128bc80461ea064a99fab916a9152))
* add license template files and post-gen hook logic ([a68e92a](https://github.com/broadsage/docker-scaffold/commit/a68e92a147099427ad6661ab3f6fb445c1f2dd79))
* add modern GitHub Discussions templates for community engagement ([e0b2d07](https://github.com/broadsage/docker-scaffold/commit/e0b2d07c0506a8af8d6529606236699b64975e46))
* add pull request template with contributor guidelines and Docker-specific checklist ([1334f5a](https://github.com/broadsage/docker-scaffold/commit/1334f5a5e4a96e3899658dc9585350829d2e2f7f))
* add question/support issue template ([d52b58c](https://github.com/broadsage/docker-scaffold/commit/d52b58cb034b02de2144e09c7a23d29995fce0d7))
* add security scanning, image signing, and SBOM generation ([4e377b3](https://github.com/broadsage/docker-scaffold/commit/4e377b38edbd7e3b30bbc4023ca045b6534571ca))
* add SPDX copyright headers to all generated templates ([38e360f](https://github.com/broadsage/docker-scaffold/commit/38e360fb9b00d8b5b5bf469feeffe9265801d0fa))
* add SPDX license headers to all project files ([2676d91](https://github.com/broadsage/docker-scaffold/commit/2676d914ec429a22683091f4ceda986a74d17508))
* add task to copy .gitignore template to project root ([e65a2ec](https://github.com/broadsage/docker-scaffold/commit/e65a2ecc536cf26fe6d9c860b1a3597b9c4e6199))
* add template versioning and update system ([b9174f8](https://github.com/broadsage/docker-scaffold/commit/b9174f804dfd0fa343b9b367ca54bd4f3cb64721))
* compliance role added ([71ddbf3](https://github.com/broadsage/docker-scaffold/commit/71ddbf34044f1e8fde648a13ae1d897a2222af26))
* **compliance:** add granular feature flag system for compliance tools ([35fb2e2](https://github.com/broadsage/docker-scaffold/commit/35fb2e2e717da0a20e3cdb14dc431afbbbce86be))
* consolidate template version management into Python ([c628bd1](https://github.com/broadsage/docker-scaffold/commit/c628bd1fa7228a998280101b2eff0fca85204c97))
* implement dependabot auto-merge workflow ([818d8ac](https://github.com/broadsage/docker-scaffold/commit/818d8ac15d98fc0e413da4ba1f3c619c396897b1))
* implement dynamic template file exclusion ([952cede](https://github.com/broadsage/docker-scaffold/commit/952ceded91fc86793c33d42018dfc9d8caf07f1a))
* implement hybrid Python venv path handling with structured _python_* variables ([98b7cad](https://github.com/broadsage/docker-scaffold/commit/98b7caddd90bd264a87dca7b12769ea446a77d0a))
* make metadata.license mandatory field in merge_config validation ([e1c4daa](https://github.com/broadsage/docker-scaffold/commit/e1c4daae8331f75343776c5ed3cded10af5ef33c))
* migrate from Dependabot to Renovate for advanced dependency management ([1328289](https://github.com/broadsage/docker-scaffold/commit/13282892a86986188c970173cc97f3569a8146f5))
* **template:** improved docker-scaffold for docker projects ([d1e21ef](https://github.com/broadsage/docker-scaffold/commit/d1e21ef457526fe726e989b139b8a4c10809511e))
* **template:** improved docker-scaffold for docker projects ([d1e21ef](https://github.com/broadsage/docker-scaffold/commit/d1e21ef457526fe726e989b139b8a4c10809511e))
* update license options with SPDX compliance ([992ba1c](https://github.com/broadsage/docker-scaffold/commit/992ba1c6c1f3072c0fd2be56c9baf6ded1333b35))
* update license options with SPDX compliance ([af55dd1](https://github.com/broadsage/docker-scaffold/commit/af55dd12f90860c362f9f010246b12d7295cc409))
* update PR templates and add Ansible Jinja2 template ([31a4dd8](https://github.com/broadsage/docker-scaffold/commit/31a4dd86e2a91f205b7bc224da473b7398593a02))
* update PR templates and add Ansible Jinja2 template ([8c0abcb](https://github.com/broadsage/docker-scaffold/commit/8c0abcb43e7f2d72b9518c7416902051c7eed2b7))


### Bug Fixes

* add push trigger to CodeQL workflow for default branch scanning ([36b4e59](https://github.com/broadsage/docker-scaffold/commit/36b4e595e45c716a9ada58f92a20d8263817df9a))
* align table separator and status column formatting in compliance script ([5812fbb](https://github.com/broadsage/docker-scaffold/commit/5812fbb792d44063e54b1b1c7a735549af248425))
* allow lowercase 'bump' and 'update' in PR titles for Dependabot ([f446553](https://github.com/broadsage/docker-scaffold/commit/f4465537b931149db0f683d76aa04490a2036922))
* change readme.md file labels ([2c48885](https://github.com/broadsage/docker-scaffold/commit/2c48885d1294a498fa2b11aaec5f998c6c75bee7))
* Change summary title ([910bf40](https://github.com/broadsage/docker-scaffold/commit/910bf40248bc8cb36fe0c02f9e77fc936b3a29d7))
* configure Renovate to add DCO sign-offs and commit bodies ([2c525f1](https://github.com/broadsage/docker-scaffold/commit/2c525f1b7ea28d1614e991bdd5c725fb6919cfbe))
* copy scripts folder to Docker image ([4d69b38](https://github.com/broadsage/docker-scaffold/commit/4d69b3841476c6d5be75270883d4da26e4d6eea6))
* correct catatonit path to /usr/bin/catatonit ([966974d](https://github.com/broadsage/docker-scaffold/commit/966974d7deb204206394ed053a16c5216f3b877d))
* correct ISO 3166-1 country codes in publiccode.yaml ([065f209](https://github.com/broadsage/docker-scaffold/commit/065f2092c1e45aa9076057f1c42d68beaf6cc43a))
* correct JavaScript syntax in MegaLinter Summary step ([6a543b1](https://github.com/broadsage/docker-scaffold/commit/6a543b12cfb8ccb476f517ffbb82068916451aee))
* discussion templates cleanup ([2651735](https://github.com/broadsage/docker-scaffold/commit/265173587485e1ae9f4e6cd8e8be49d533eaa9e0))
* **docs:** commit scopes removed ([8b5bca0](https://github.com/broadsage/docker-scaffold/commit/8b5bca00ec2dbff8d299a28c4f4ed0cc05f0e460))
* inline short_name computation in project_description ([a000d7b](https://github.com/broadsage/docker-scaffold/commit/a000d7b70fdad1e1c14214546f6a0f301497d012))
* make read command POSIX-compliant in template:update task ([de3427f](https://github.com/broadsage/docker-scaffold/commit/de3427f620201002473549e058712c3b8293962c))
* markdown linting and add CODE_OF_CONDUCT template ([bf61b82](https://github.com/broadsage/docker-scaffold/commit/bf61b822a7c71cebf54b5d65a7214cf74420d56d))
* publiccode.yaml validation and Docker stdin handling ([e5fa6ae](https://github.com/broadsage/docker-scaffold/commit/e5fa6ae631061e9d9500f6915feb1c4c42f3da18))
* quote GITHUB_ENV variable in compliance workflow ([129932a](https://github.com/broadsage/docker-scaffold/commit/129932af2e9539384f6700b5472af6364d73c549))
* remove {% raw %} tags to enable Jinja2 feature evaluation ([f302f5f](https://github.com/broadsage/docker-scaffold/commit/f302f5f22a3b8590948fb4c1411b2024329a5dfe))
* remove invalid category property from discussion templates ([8283369](https://github.com/broadsage/docker-scaffold/commit/8283369f8787abc153bdaf774a67e234b539b70f))
* remove invalid queries parameter from CodeQL workflow ([e080ed2](https://github.com/broadsage/docker-scaffold/commit/e080ed2482819d8f0f2ebf063c3f212758cbb651))
* remove strict lowercase header requirement from conform config ([864f817](https://github.com/broadsage/docker-scaffold/commit/864f8170a001a8a5bd3eb569a5fd3ec49d2ed4f1))
* remove strict lowercase header requirement from conform config ([262494e](https://github.com/broadsage/docker-scaffold/commit/262494e6fdd0681b422d00cd68a98bcdf649ee31))
* remove template-snyk workflow ([664ed98](https://github.com/broadsage/docker-scaffold/commit/664ed98186a170c617a9d0c5be02d7ec04a0fe13))
* remove unnecessary separator line in CODE_OF_CONDUCT ([3171ed9](https://github.com/broadsage/docker-scaffold/commit/3171ed9afac1a1370e7481c6027dfcaf4fe2d169))
* rename release-please config file without leading dot ([e554416](https://github.com/broadsage/docker-scaffold/commit/e55441611619e97bb7d2248edef88f8ea5725c97))
* resolve Jinja2 template syntax conflict with Task variables ([4798aa0](https://github.com/broadsage/docker-scaffold/commit/4798aa01e0cb7475f09a50c1c056103f5b7c0998))
* resolve linting issues and protect Jinja2 templates from formatting ([9e44c52](https://github.com/broadsage/docker-scaffold/commit/9e44c521827bb619c6f19dbcc46d768736e83fdc))
* resolve shellcheck SC2086 warnings and cleanup merged_config.yaml references ([a29cb82](https://github.com/broadsage/docker-scaffold/commit/a29cb826cdc862aa00a3b2660129c4e54402d27b))
* resolve yamllint errors in workflow files ([05e0e35](https://github.com/broadsage/docker-scaffold/commit/05e0e3566c8be6a705de0ec7e5eacd0bb2fbc378))
* restructure announcements template for GitHub compatibility ([4c8d068](https://github.com/broadsage/docker-scaffold/commit/4c8d068c0446e21130959122527853b0fafbe4d4))
* simplify _python_executable variable to avoid circular evaluation ([e1b1884](https://github.com/broadsage/docker-scaffold/commit/e1b1884640dfd1601541832b58c4e37f99e6b0af))
* simplify announcements template to fix GitHub rendering ([3352af2](https://github.com/broadsage/docker-scaffold/commit/3352af2a639a20039f8257c12138b3fdfa590022))
* simplify discussion templates to minimal format ([4f81d11](https://github.com/broadsage/docker-scaffold/commit/4f81d114d5ac6e2aa6e380f872eac943bfefa70d))
* template error fix updated ([0097f94](https://github.com/broadsage/docker-scaffold/commit/0097f94dc92210880d6b648eff333fd82eebb20d))
* update .dockerignore to include required build files ([01f8c3c](https://github.com/broadsage/docker-scaffold/commit/01f8c3cb712defa2d2ab07df3a7b70ab64264a9a))
* update actions/cache to v4 to avoid deprecation ([4056d67](https://github.com/broadsage/docker-scaffold/commit/4056d6709afb9535739a48a09ec07a1c7fa434f0))
* update CodeQL Action from v3 to v4 ([bd31f8d](https://github.com/broadsage/docker-scaffold/commit/bd31f8d22b9c74405afcb98012c74077f44006b0))
* update post_gen_project.py to reference project_slug ([56655d0](https://github.com/broadsage/docker-scaffold/commit/56655d00e5b5ef642059d8053fae08bc0576c1a8))
* update Taskfile.yml to use full cookiecutter variable references ([fdec094](https://github.com/broadsage/docker-scaffold/commit/fdec094f39c8936293ad96cde7cf40eb36169972))
* use COOKIECUTTER_TEMPLATE_FOLDER env var to locate license templates ([3ffa90d](https://github.com/broadsage/docker-scaffold/commit/3ffa90dd5002580ad44c2395a7a508ac440ccb6d))
* yaml file renamed ([217f3e9](https://github.com/broadsage/docker-scaffold/commit/217f3e91fd0deae55b1934fad38049855fba8f95))


### Performance Improvements

* optimize workflow triggers to reduce redundant runs ([8a3ab27](https://github.com/broadsage/docker-scaffold/commit/8a3ab272c287efc91f22e447b98cd2faccfc1c10))


### Reverts

* restore detailed discussion templates with form structure ([fd01b31](https://github.com/broadsage/docker-scaffold/commit/fd01b31f1d39df6cbd8fba9eea4e4ae4b38913a9))


### Documentation

* add documentation role and expand template-usage guide ([042aeaf](https://github.com/broadsage/docker-scaffold/commit/042aeaf389a249d8876e5f2606948715b1ab2619))
* fix markdown linting errors and add CONTRIBUTING.md ([f1baec1](https://github.com/broadsage/docker-scaffold/commit/f1baec1feba5c066340a3d99c27665b31e9c7030))
* update documentation formatting ([6d96bab](https://github.com/broadsage/docker-scaffold/commit/6d96bab443554c86108433b43445f52de2ca6fb9))
* update README and add CODE_OF_CONDUCT ([23a9b14](https://github.com/broadsage/docker-scaffold/commit/23a9b14946dcf26b71142aead08179865e1ebd55))


### Code Refactoring

* add date to timestamp display in compliance output ([c0bed1a](https://github.com/broadsage/docker-scaffold/commit/c0bed1ad385c22736778f03bdc422b450917043f))
* auto-cleanup merged_config.yaml after ansible generation ([73e1b76](https://github.com/broadsage/docker-scaffold/commit/73e1b763c37f577888b51d57f916f7c073aa1e9b))
* change container image name to scaffold ([acf5709](https://github.com/broadsage/docker-scaffold/commit/acf5709b3df1c38039fb7388e03e96e38dbfe9e6))
* clean up compliance workflow - remove duplication and improve clarity ([a2e241e](https://github.com/broadsage/docker-scaffold/commit/a2e241e70c22fd56f9ad1c9da55095a02a31f495))
* **compliance:** funtion name changed ([b9cdc86](https://github.com/broadsage/docker-scaffold/commit/b9cdc869c9e307ba2a551d6f58c13a544456d7d2))
* **compliance:** update conform and megalinter configs to follow best practices ([54bb4ac](https://github.com/broadsage/docker-scaffold/commit/54bb4acb61000961e1dc405bedfea687b413587c))
* consolidate version variables to global scope ([dc17a41](https://github.com/broadsage/docker-scaffold/commit/dc17a4190666564d96654937dc03590755ab18bb))
* convert all placeholder text to single-line format ([6463fed](https://github.com/broadsage/docker-scaffold/commit/6463fedbccfbc036349ef6c99cb2d55306516253))
* eliminate code duplication and improve code quality ([c4f8165](https://github.com/broadsage/docker-scaffold/commit/c4f8165193e7210d6cba6f7ba06c86a1687accb6))
* file extension change ([3e73d67](https://github.com/broadsage/docker-scaffold/commit/3e73d672cfee01c1a54278f29586b7aae07212b3))
* hide computed fields from user prompts using underscore prefix ([acbab78](https://github.com/broadsage/docker-scaffold/commit/acbab78181b9ad6be25c8d97779466ead2baa0bc))
* improve entrypoint.sh with best practices ([fab22e2](https://github.com/broadsage/docker-scaffold/commit/fab22e25b49d6ca3d650c0c7b0471bd1b20fa0aa))
* improve workflow job names for clarity ([8e4637f](https://github.com/broadsage/docker-scaffold/commit/8e4637f0cf456782e7a2c4d6f22b89f905a00635))
* integrate compliance.py into ansible compliance role ([df22ed6](https://github.com/broadsage/docker-scaffold/commit/df22ed61c6a4051f9c30938ab096d70c3e88a125))
* make configuration merger fully dynamic ([42187ce](https://github.com/broadsage/docker-scaffold/commit/42187ce7bcf03f18a79eedeb7285303638125501))
* migrate from common.yml variable mapping to direct merged config access ([ec56f0a](https://github.com/broadsage/docker-scaffold/commit/ec56f0a690bce15e928b00115743fd795a279870))
* modernize compliance workflow with industry best practices ([7c6bf8e](https://github.com/broadsage/docker-scaffold/commit/7c6bf8e76860f6a2efab952bf3c525a43fbe0a8d))
* modernize Dockerfile and add multi-arch CI/CD ([b543a70](https://github.com/broadsage/docker-scaffold/commit/b543a7001668c9ec7ec1ca9bb14752eb9584862d))
* modernize post_gen output with event-based formatting and timestamps ([c7b00ac](https://github.com/broadsage/docker-scaffold/commit/c7b00acc6457bcbbcfa0e26026ba4e7d3aa02290))
* move bootstrap files to cookiecutter template ([7543e96](https://github.com/broadsage/docker-scaffold/commit/7543e96f4b32243ec1eb07c3480b794292add5ef))
* move license files back to {{cookiecutter.project_slug}} for simplicity ([7a57b9a](https://github.com/broadsage/docker-scaffold/commit/7a57b9a455f685a91f350343814679f9ab38ef2e))
* move requirements.txt to project root ([6d73bc5](https://github.com/broadsage/docker-scaffold/commit/6d73bc54f97d4700cb5ef47edac6e5dc1412817c))
* move welcome message to visible section in pull request template ([058ff46](https://github.com/broadsage/docker-scaffold/commit/058ff46784885fd22458b99307565a21066d1738))
* optimize compliance and release workflows ([68b13f6](https://github.com/broadsage/docker-scaffold/commit/68b13f6afcd92cbbbed012218dec907754d35f00))
* remove artifact uploads from compliance workflow ([0476c52](https://github.com/broadsage/docker-scaffold/commit/0476c521f664a8764fa605d4d1a0f09de537d61b))
* remove optional title field from discussion templates ([afb0a62](https://github.com/broadsage/docker-scaffold/commit/afb0a621cc507a40b9b7331336e245e9442fd517))
* remove publiccode.yml compliance support ([43cd42f](https://github.com/broadsage/docker-scaffold/commit/43cd42fa1b9e8d8d4c36fbd10d377bf6a8b82b4f))
* remove SARIF upload from MegaLinter workflow ([c23cdd8](https://github.com/broadsage/docker-scaffold/commit/c23cdd8c37664fa56f39318b2d1b8e8c10484021))
* remove SCRIPTS_DIR var, hardcode scripts path ([a8ddab0](https://github.com/broadsage/docker-scaffold/commit/a8ddab00339c65555fbb5b1ac3b49880d6b3ecb8))
* rename bump_version.py to release.py with extensible architecture ([a4b5579](https://github.com/broadsage/docker-scaffold/commit/a4b5579920a08753f35501ea81ea2b1ef7ac24e4))
* rename issue templates to use hyphens instead of underscores ([8337501](https://github.com/broadsage/docker-scaffold/commit/8337501f8f424b44b0f1af9a06783fb5938afc9a))
* rename merge_config.py to config.py ([82d411e](https://github.com/broadsage/docker-scaffold/commit/82d411e7346b912700acba45b9505e10b4adc133))
* rename workflow to Pre-merge Validation & Compliance ([b32c6ad](https://github.com/broadsage/docker-scaffold/commit/b32c6ad7a1efc7421b31ef5dc0ef0ff4abcdff13))
* rename YAML files from .yml to .yaml extension ([0472967](https://github.com/broadsage/docker-scaffold/commit/047296704158350843691bb20da60145f0ecd5bf))
* rename YAML files from .yml to .yaml extension ([cdd617d](https://github.com/broadsage/docker-scaffold/commit/cdd617dab8a49b1f2b490b56f7d396cd2ae9cd82))
* reorganize scripts and simplify Taskfile configuration ([397fcf0](https://github.com/broadsage/docker-scaffold/commit/397fcf0440c0f6951375360ac01294fecd1acd56))
* replace Trivy with Snyk for container security scanning ([6b16945](https://github.com/broadsage/docker-scaffold/commit/6b16945978efe2943d95ee2aba16b6ddd790830c))
* restructure license files to templates/licenses/ directory ([ee71729](https://github.com/broadsage/docker-scaffold/commit/ee717293da32fc9c08ed685ba10c7150771c6417))
* simplify docker-build to only trigger on release tags ([1ed1e58](https://github.com/broadsage/docker-scaffold/commit/1ed1e582027137042474ec7253afdbaf2b07d71e))
* simplify project_slug to use direct computation ([1ceb060](https://github.com/broadsage/docker-scaffold/commit/1ceb0600c2ce34557f6037f51a99cd3e1a3426f1))
* simplify project_slug to use direct computation ([eb8739b](https://github.com/broadsage/docker-scaffold/commit/eb8739b8324b09b75daec6c89c497d3b08cde0c3))
* simplify project_slug to use direct computation ([b3c064a](https://github.com/broadsage/docker-scaffold/commit/b3c064a281ea30826e0dd1db3429f71c92fdffb1))
* split github tasks into setup and cleanup modules ([fde3d0c](https://github.com/broadsage/docker-scaffold/commit/fde3d0caa72078f9fe5aa9d8bf119783624fde54))
* split license function into download and lint steps ([11f744d](https://github.com/broadsage/docker-scaffold/commit/11f744db5b02635efd3690a3b4d15e7de7cfa9a6))
* split license function into download and lint steps ([ebab3a4](https://github.com/broadsage/docker-scaffold/commit/ebab3a4d1c5b28a3b78d0fd622a946bcc8ad66f7))
* standardize issue template prerequisites and simplify question environment field ([f1edc40](https://github.com/broadsage/docker-scaffold/commit/f1edc40c7bc5013425d165bc56f3c91425c03152))
* streamline CodeQL workflow to Python security analysis only ([879a0fa](https://github.com/broadsage/docker-scaffold/commit/879a0fa22f6f3eb059b2fa29a0c1611315ef7398))
* **taskfile:** rename tasks to follow cleaner naming conventions ([2a469f1](https://github.com/broadsage/docker-scaffold/commit/2a469f1071bb152e06c7cb1e4622338b56aaaca7))
* test docker-scaffold on current project instead of temp directory ([015ce75](https://github.com/broadsage/docker-scaffold/commit/015ce75b2ce2ecfec82a10a86121d70a58fe4147))
* update .dockerignore to follow industry best practices ([c406ca3](https://github.com/broadsage/docker-scaffold/commit/c406ca3957d307d40bc2c6848b946156d7911f60))
* update compliance and configuration files ([989763c](https://github.com/broadsage/docker-scaffold/commit/989763c21c87a68621402f060a5154d743521f4b))
* update config.yml contact link emojis to modern versions ([399ee6f](https://github.com/broadsage/docker-scaffold/commit/399ee6fe095e361fb0cf6d83319d19699c3b10b5))
* update discussion templates with welcoming greetings and best practices ([6a9d3a7](https://github.com/broadsage/docker-scaffold/commit/6a9d3a776d0e0b862c6dd953e1c88e4a8963d2da))
* update discussion templates with welcoming greetings and best practices ([1832a69](https://github.com/broadsage/docker-scaffold/commit/1832a69d74030c23c7d613c9a5a3a243f49c1b66))
* update discussion templates with welcoming greetings and best practices ([34cfc93](https://github.com/broadsage/docker-scaffold/commit/34cfc93ced837edd1f230b502de056f3ba957b1a))
* update discussion templates with welcoming greetings and best practices ([2d6494a](https://github.com/broadsage/docker-scaffold/commit/2d6494ae7fb14123caab0c454a148cc61623e5e0))


### Continuous Integration

* add explicit latest image tag on default branch ([09b6caa](https://github.com/broadsage/docker-scaffold/commit/09b6caa5b47a4254f8c7f68fe1179736e60fae03))
* **conform:** enhance commit policy and validation workflows ([2d4dc5a](https://github.com/broadsage/docker-scaffold/commit/2d4dc5a4a2524576b7d2c500af0deabd401a37da))
* update docker-build workflow formatting ([5d6fc37](https://github.com/broadsage/docker-scaffold/commit/5d6fc373b5ce9b65e7568691f3bcd2a60bafda01))
