import fs from 'fs';
import path from 'path';
import Papa from 'papaparse';
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
  try {
    const filePath = path.join(process.cwd(), '..', 'backend', 'data', 'optimized_schedule.csv');
    const fileContent = fs.readFileSync(filePath, 'utf8');
    
    const parsed = Papa.parse(fileContent, {
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true
    });
    
    return NextResponse.json(parsed.data);
  } catch (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
}
