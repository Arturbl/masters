targetBuild ?= dev

BUNDLE=rbenv exec bundle _2.4.10_

setup:
	brew update
	brew upgrade
	brew cleanup
	brew install rbenv 
	rbenv install -s
	rbenv exec gem update --system --no-document --quiet
	rbenv exec gem install bundler -v 2.4.10
	rbenv rehash
	$(BUNDLE) install

clean:
	flutter clean

libs-update:
	flutter pub upgrade --major-versions

app:
	flutter packages run app build --delete-conflicting-outputs

build-run:
	flutter clean
	flutter pub get

apk:
	flutter build apk --dart-define=targetBuild=$(targetBuild) --split-per-abi --target-platform android-arm,android-arm64,android-x64
	open ./build/app/outputs/flutter-apk/
single-apk:
	flutter build apk --dart-define=targetBuild=$(targetBuild)
	open ./build/app/outputs/flutter-apk/

web-build:
	flutter clean
	flutter pub get
	flutter build web   --base-href '/'

dev-deploy:
	sh dev-deploy.sh

deploy:
	sh web-deploy

docker-dev-apk:
	sh build-dev-apk.sh

run-watch:
	flutter pub get
	flutter packages run app build watch --delete-conflicting-outputs --use-polling-watcher
