//
//  ContentView.swift
//  dump
//
//  Created by Griffin Tarpenning on 5/28/23.
//

import SwiftUI

struct ContentView: View {
  @ObservedObject var vm = VoiceViewModel()

  @State private var showingList = false
  @State private var showingAlert = false
  @State private var effect1 = false
  @State private var effect2 = false
  @State private var isLoading = false

  var body: some View {
    NavigationView {
      ZStack {
        VStack {
          HStack {
            Spacer()
            NavigationLink(destination: Text("Settings")) {
              Image(systemName: "gear")
                .resizable()
                .frame(width: 40, height: 40)
                .padding(.trailing, 18)
            }
          }
          Spacer()
          if vm.whisperText != "" {
            TagClusterView(text: vm.whisperText + "...", tags: vm.tags)
          } else {
            if vm.isRecording {
              VStack(alignment: .center) {
                HStack(spacing: 5) {
                  Image(systemName: vm.isRecording && vm.toggleColor ? "circle.fill" : "circle")
                    .font(.system(size: 10))
                    .foregroundColor(.red)
                  Text("Recording")
                }
                Text(vm.timer)
                  .font(.system(size: 60))
                  .foregroundColor(.gray)
              }
            } else if vm.loading {
              Group {
                Circle()
                  .trim(from: 0, to: 0.7)
                  .stroke(Color.green, lineWidth: 5)
                  .frame(width: 100, height: 100)
                  .rotationEffect(Angle(degrees: isLoading ? 360 : 0))
                  .animation(
                    Animation.default.repeatForever(autoreverses: false),
                    value: isLoading
                  )
                  .onAppear {
                    isLoading = true
                  }
              }
            } else {
              VStack {
                Text("dump your day")
                  .foregroundColor(.gray)
                  .fontWeight(.bold)
                  .font(.system(size: 30))
                  .padding(.bottom, 5)
              }
              .frame(width: 300, height: 100, alignment: .bottom)
            }
          }

          Spacer()
          Spacer()

          // RECORD BUTTON
          if !vm.loading && vm.whisperText == "" {
            ZStack {
              Circle()
                .frame(width: 50, height: 50)
                .foregroundColor(Color(.red))
                .scaleEffect(effect2 ? 1 : 1.5)
                .onAppear {
                  self.effect1.toggle()
                }
              Image(systemName: vm.isRecording ? "stop.circle.fill" : "mic.circle.fill")
                .foregroundColor(.white)
                .font(.system(size: 50))
                .onTapGesture {
                  if vm.isRecording == true {
                    vm.stopRecording()
                  } else {
                    vm.startRecording()

                  }
                }

            }
          }

          Spacer()
          HStack {
            Spacer()
            NavigationLink(destination: Text("Home View")) {
              ZStack {
                Image(systemName: "house")
                  .resizable()
                  .frame(width: 45, height: 45)
              }
            }
            .padding(.trailing, 20)
            NavigationLink(destination: CalendarInsightView()) {
              ZStack {
                Image(systemName: "calendar")
                  .resizable()
                  .frame(width: 45, height: 45)
              }
              .padding(.leading, 20)
            }
            Spacer()
          }
        }
        .padding(.bottom, 10)
        .padding(.leading, 25)
        .padding(.trailing, 25)
      }
    }
  }
}

struct ContentView_Previews: PreviewProvider {
  static var previews: some View {
    ContentView()
  }
}
